from .models import Client, MailingList, Message
from django.test import TestCase
from datetime import datetime
from json import dumps
import pytz

utc=pytz.UTC

# Model unit tests
class ModelsTests(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            id=0,
            phone="71111111111",
            code="936",
            tag="test_tag",
            timezone="Africa/Abidjan"
        )
        self.time = datetime.now()
        self.mailinglist = MailingList(
            id=0,
            startTime=self.time,
            msg="test_message",
            code="936",
            tag="test_tag",
            endTime=self.time
        )
        self.message = Message(
            id=0,
            time=self.time,
            status="Waiting",
            listId=self.mailinglist,
            clientId=self.client
        )

    def tearDown(self):
        del self.client

    def test_client_creation(self):
        self.assertTrue(self.client.id == 0)
        self.assertTrue(self.client.phone == "71111111111")
        self.assertTrue(self.client.code == "936")
        self.assertTrue(self.client.tag == "test_tag")
        self.assertTrue(self.client.timezone == "Africa/Abidjan")
    
    def test_mailinglist_creation(self):
        self.assertTrue(self.mailinglist.id == 0)
        self.assertTrue(self.mailinglist.startTime == self.time)
        self.assertTrue(self.mailinglist.msg == "test_message")
        self.assertTrue(self.mailinglist.tag == "test_tag")
        self.assertTrue(self.mailinglist.code == "936")
        self.assertTrue(self.mailinglist.endTime == self.time)

    def test_message_creation(self):
        self.assertTrue(self.message.id == 0)
        self.assertTrue(self.message.time == self.time)
        self.assertTrue(self.message.status == "Waiting")
        self.assertTrue(self.message.listId == self.mailinglist)
        self.assertTrue(self.message.clientId == self.client)

# Viewset functional tests
class ClientViewTests(TestCase):

    def setUp(self):
        self.response_post = self.client.post('http://127.0.0.1:8000/api/client/', dumps({
            "id":"0",
            "phone":"71111111111",
            "code":"936",
            "tag":"test_tag",
            "timezone":"Africa/Abidjan"
        }), content_type="application/json")
        self.response_get = self.client.get("http://127.0.0.1:8000/api/client/0/")
        self.response_update = self.client.patch('http://127.0.0.1:8000/api/client/0/', dumps({
            "id":"0",
            "phone":"76231451231",
            "code":"551",
            "tag":"new_tag",
            "timezone":"Africa/Abidjan"
        }), content_type="application/json")
        self.response_validation = self.client.post('http://127.0.0.1:8000/api/client/', dumps({
            "id":"0",
            "phone":"751",
            "code":"1",
            "tag":"test_tag",
            "timezone":"Africa/Abidjan"
        }), content_type="application/json")
        self.response_delete = self.client.delete("http://127.0.0.1:8000/api/client/0/")
        

    def test_client_creation(self):
        self.assertTrue(self.response_post.status_code == 201)
        self.assertTrue(self.response_post.json()['id'] == "0")
        self.assertTrue(self.response_post.json()['phone'] == "71111111111")
        self.assertTrue(self.response_post.json()['code'] == "936")
        self.assertTrue(self.response_post.json()['tag'] == "test_tag")
        self.assertTrue(self.response_post.json()['timezone'] == "Africa/Abidjan")
    
    def test_client_delete(self):
        self.assertTrue(self.response_delete.status_code == 204)

    def test_client_update(self):
        self.assertTrue(self.response_update.status_code == 200)
        self.assertTrue(self.response_update.json()['id'] == "0")
        self.assertTrue(self.response_update.json()['phone'] == "76231451231")
        self.assertTrue(self.response_update.json()['code'] == "551")
        self.assertTrue(self.response_update.json()['tag'] == "new_tag")
        self.assertTrue(self.response_update.json()['timezone'] == "Africa/Abidjan")

    def test_client_get(self):
        self.assertTrue(self.response_get.status_code == 200)
        self.assertTrue(self.response_get.json()['id'] == "0")
        self.assertTrue(self.response_get.json()['phone'] == "71111111111")
        self.assertTrue(self.response_get.json()['code'] == "936")
        self.assertTrue(self.response_get.json()['tag'] == "test_tag")
        self.assertTrue(self.response_get.json()['timezone'] == "Africa/Abidjan")
    
    def test_client_validation(self):
        self.assertTrue(self.response_validation.status_code == 400)
        self.assertTrue('id' in self.response_validation.json())
        self.assertTrue('phone' in self.response_validation.json())
        self.assertTrue('code' in self.response_validation.json())

class MailingListViewTests(TestCase):

    def setUp(self):
        self.current_time = datetime.now()
        self.response_post = self.client.post('http://127.0.0.1:8000/api/mailinglist/', dumps({
            "id":"0",
            "startTime": str(self.current_time),
            "msg": "test_msg",
            "code":"936",
            "tag":"test_tag",
            "endTime": str(self.current_time),
        }), content_type="application/json")
        self.response_get = self.client.get("http://127.0.0.1:8000/api/mailinglist/0/")
        self.response_update = self.client.patch('http://127.0.0.1:8000/api/mailinglist/0/', dumps({
            "id":"0",
            "startTime": str(self.current_time),
            "msg": "new_msg",
            "code":"535",
            "tag":"new_tag",
            "endTime": str(self.current_time),
        }), content_type="application/json")
        self.response_validation = self.client.post('http://127.0.0.1:8000/api/mailinglist/', dumps({
            "id":"0",
            "startTime": str(self.current_time),
            "msg": "new_msg",
            "code":"1",
            "tag":"new_tag",
            "endTime": str(self.current_time),
        }), content_type="application/json")
        self.response_delete = self.client.delete("http://127.0.0.1:8000/api/mailinglist/0/")
        

    def test_mailinglist_creation(self):
        self.assertTrue(self.response_post.status_code == 201)
        self.assertTrue(self.response_post.json()['id'] == "0")
        self.assertTrue(datetime.strptime(self.response_post.json()['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_post.json()['code'] == "936")
        self.assertTrue(self.response_post.json()['tag'] == "test_tag")
        self.assertTrue(datetime.strptime(self.response_post.json()['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_post.json()['msg'] == "test_msg")
    
    def test_mailinglist_delete(self):
        self.assertTrue(self.response_delete.status_code == 204)

    def test_mailinglist_update(self):
        self.assertTrue(self.response_update.status_code == 200)
        self.assertTrue(self.response_update.json()['id'] == "0")
        self.assertTrue(datetime.strptime(self.response_update.json()['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_update.json()['code'] == "535")
        self.assertTrue(self.response_update.json()['tag'] == "new_tag")
        self.assertTrue(datetime.strptime(self.response_update.json()['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_update.json()['msg'] == "new_msg")

    def test_mailinglist_get(self):
        self.assertTrue(self.response_get.status_code == 200)
        self.assertTrue(self.response_get.json()['id'] == "0")
        self.assertTrue(datetime.strptime(self.response_get.json()['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")== self.current_time)
        self.assertTrue(self.response_get.json()['code'] == "936")
        self.assertTrue(self.response_get.json()['tag'] == "test_tag")
        self.assertTrue(datetime.strptime(self.response_get.json()['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_get.json()['msg'] == "test_msg")
    
    def test_mailinglist_validation(self):
        self.assertTrue(self.response_validation.status_code == 400)
        self.assertTrue('id' in self.response_validation.json())
        self.assertTrue('code' in self.response_validation.json())

class MessageViewTests(TestCase):

    def setUp(self):
        self.current_time = datetime.now()
        self.client.post('http://127.0.0.1:8000/api/client/', dumps({
            "id":"0",
            "phone":"71111111111",
            "code":"936",
            "tag":"test_tag",
            "timezone":"Africa/Abidjan"
        }), content_type="application/json")
        self.client.post('http://127.0.0.1:8000/api/mailinglist/', dumps({
            "id":"0",
            "startTime": str(self.current_time),
            "msg": "test_msg",
            "code":"936",
            "tag":"test_tag",
            "endTime": str(self.current_time),
        }), content_type="application/json")
        self.response_post = self.client.post('http://127.0.0.1:8000/api/message/', dumps({
            "id":0,
            "time":str(self.current_time),
            "clientId":"0",
            "listId":"0",
            "status":"Sending"
        }), content_type="application/json")
        self.response_get = self.client.get("http://127.0.0.1:8000/api/message/0/")
        self.response_update = self.client.patch('http://127.0.0.1:8000/api/message/0/', dumps({
            "id":0,
            "time":str(self.current_time),
            "clientId":"0",
            "listId":"0",
            "status":"Waiting"
        }), content_type="application/json")
        self.response_delete = self.client.delete("http://127.0.0.1:8000/api/message/0/")

    def test_message_creation(self):
        self.assertTrue(self.response_post.status_code == 201)
        print(self.response_post.json()['id'])
        self.assertTrue(self.response_post.json()['id'] == 0)
        self.assertTrue(datetime.strptime(self.response_post.json()['time'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_post.json()['clientId'] == "0")
        self.assertTrue(self.response_post.json()['listId'] == "0")
        self.assertTrue(self.response_post.json()['status'] == "Sending")
    
    def test_message_delete(self):
        self.assertTrue(self.response_delete.status_code == 204)

    def test_message_update(self):
        self.assertTrue(self.response_update.status_code == 200)
        self.assertTrue(self.response_update.json()['id'] == 0)
        self.assertTrue(datetime.strptime(self.response_update.json()['time'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_update.json()['clientId'] == "0")
        self.assertTrue(self.response_update.json()['listId'] == "0")
        self.assertTrue(self.response_update.json()['status'] == "Waiting")

    def test_message_get(self):
        self.assertTrue(self.response_get.status_code == 200)
        self.assertTrue(self.response_get.json()['id'] == 0)
        self.assertTrue(datetime.strptime(self.response_get.json()['time'], "%Y-%m-%dT%H:%M:%S.%fZ") == self.current_time)
        self.assertTrue(self.response_get.json()['clientId'] == "0")
        self.assertTrue(self.response_get.json()['listId'] == "0")
        self.assertTrue(self.response_get.json()['status'] == "Sending")