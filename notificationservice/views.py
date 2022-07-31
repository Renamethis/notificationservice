from .serializers import ClientSerializer, MalingListSerializer, MessageSerializer
from .models import Client, MailingList, Message
from rest_framework import viewsets
from rest_framework.decorators import action
from json import loads

class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

class MailingListViewset(viewsets.ModelViewSet):
    queryset = MailingList.objects.all()
    serializer_class = MalingListSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']