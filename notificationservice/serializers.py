from rest_framework import serializers
from .models import Client, MailingList, Message
from json import loads 

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'code', 'tag', 'timezone']

class MalingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ['id', 'startTime', 'message', 'code', 'tag', 'endTime']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'time', 'status', 'listId', 'clientId']