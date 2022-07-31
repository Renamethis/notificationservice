from rest_framework.routers import DefaultRouter
from notificationservice.models import Message
from notificationservice.views import ClientViewset, MailingListViewset, MessageViewset
router = DefaultRouter()
router.register(r'client', ClientViewset, basename='client')
router.register(r'mailinglist', MailingListViewset, basename='mailinglist')
router.register(r'message', MessageViewset, basename='message')
urlpatterns = [
    *router.urls,
]