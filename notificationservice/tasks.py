from threading import currentThread
from .celery import app
from celery.utils.log import get_task_logger
from datetime import timedelta
from .models import Client, MailingList, Message
from django.db.models import Max
from datetime import datetime

logger = get_task_logger(__name__)

@app.task
def send_messages():

    for mailingList in MailingList.objects.all():
        messages = Message.objects.filter(listId=mailingList.id)
        if(not messages):
            continue
        clients = Client.objects.filter(code=mailingList.code, tag=mailingList.tag)
        for client in clients:
            message = Message.objects.aggregate(Max('id'))

            id = 0
            if(message):
                id = message.id

            currentTime = datetime.now()
            status = "Waiting"
            if(mailingList.startTime < currentTime and currentTime < mailingList.endTime):
                status = "Sent"
            elif(mailingList.endTime < currentTime):
                status = "Overdue"

            message = Message.objects.create(
                id=id,
                time=currentTime,
                status=status,
                listId = mailingList.id,
                clientId = client.id
            )
            message.save()
    