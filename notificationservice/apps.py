from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'

class MailingListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailinglist'

class MessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message'