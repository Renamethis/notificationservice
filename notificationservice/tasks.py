from .celery import app
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Client, MailingList, Message
from django.db.models import Max
from datetime import datetime
from json import dumps
import requests
import pytz

# API configuration
API_URL = "https://probe.fbrq.cloud/v1/send/0"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA2MTkxMzgsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Im9rbG9wb2ZhIn0.ZJtYdaVcInobCaZbKx7XPlEGkPMjZKRJJRuJuTgkRPk"

# Timezone 
utc=pytz.UTC
# Initialize celery logger
logger = get_task_logger(__name__)

# Create new message object
def create_message(id, currentTime, status, mailingList, client):
    message = Message.objects.create(
        id=id,
        time=currentTime,
        status=status,
        listId = mailingList,
        clientId = client
    )
    message.save()

# Main periodic celery task for sending messages to the clients
@app.task
def send_messages():
    currentTime = datetime.now()
    # Iterate all of the mailing lists and find waiting messages
    for mailingList in MailingList.objects.all():
        messages = Message.objects.filter(listId=mailingList.id)
        waiting_messages = messages.filter(status="Waiting")
        if(messages and not waiting_messages):
            continue
        elif(waiting_messages):
            # Check all of the waiting messages
            for message in messages:
                currentTime = datetime.now()
                clients = Client.objects.filter(code=mailingList.code).filter(tag=mailingList.tag)
                for client in clients:
                    if(mailingList.startTime < utc.localize(currentTime) and \
                       utc.localize(currentTime) < mailingList.endTime):
                        send.delay(message.id, client.phone, mailingList.msg)
            continue
        # Find all clients for given mailing list
        clients = Client.objects.filter(code=mailingList.code).filter(tag=mailingList.tag)
        for client in clients:
            # Find max message id
            message = Message.objects.aggregate(Max('id'))
            id = 0
            if(message['id__max'] is not None):
                id = message['id__max'] + 1
            # Create message with required time status
            if(mailingList.startTime.replace(tzinfo=utc) < utc.localize(currentTime) and \
               utc.localize(currentTime) < mailingList.endTime.replace(tzinfo=utc)):
                logger.info(id)
                create_message(id, currentTime, "Sending", mailingList, client)
                send.delay(id, client.phone, mailingList.msg)
            elif(utc.localize(currentTime) > mailingList.endTime.replace(tzinfo=utc)):
                create_message(id, currentTime, "Overdue", mailingList, client)
            elif(utc.localize(currentTime) < mailingList.startTime.replace(tzinfo=utc)):
                create_message(id, currentTime, "Waiting", mailingList, client)

# Shared task to send message on the external API
@shared_task(bind=True)
def send(self, id, phone, message):
    try:
        # Send request on server
        headers = {'Authorization': 'Bearer ' + TOKEN}
        response = requests.post(API_URL, data=dumps({
            "id": 0,
            "phone": phone,
            "text": message
        }), headers=headers)
        if(response.status_code != 200):
            raise Exception("API broken")
        # Update message entry in queryset
        message = Message.objects.get(id=id)
        message.status = "Sent"
        message.time = datetime.now()
        message.save()
    except Exception as e:
        logger.error(e)
        # Retry task if exception was received
        raise self.retry(exc=e, countdown=5)