from django.db import models
from django.core.exceptions import ValidationError
import re
import pytz

# Get all existing timezones
TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

# Phone number validator
def phone_validator(value):
    if(not re.match(r'(7)\d{10}(?!\d)', value)):
            raise ValidationError('Phone number is incorrect.')

# Operator code validator
def code_validator(value):
    if(not re.match('(?<!\d)\d{3}(?!\d)', value)):
        raise ValidationError('Operator Code is incorrect.')

# Client django model
class Client(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    phone = models.CharField(max_length=11, validators=[phone_validator])
    code = models.CharField(max_length=3, validators=[code_validator])
    tag = models.CharField(max_length=100)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

# MailingList django model
class MailingList(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    startTime = models.DateTimeField()
    msg = models.CharField(max_length=500)
    code = models.CharField(max_length=3, validators=[code_validator])
    tag = models.CharField(max_length=100)
    endTime = models.DateTimeField()

# Message django model
class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    status = models.CharField(max_length=20)
    listId = models.ForeignKey('notificationservice.MailingList', on_delete=models.CASCADE)
    clientId = models.ForeignKey('notificationservice.Client', on_delete=models.CASCADE)