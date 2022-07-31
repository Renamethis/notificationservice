from rest_framework.routers import DefaultRouter
from notificationservice.models import Message
from notificationservice.views import ClientViewset, MailingListViewset, MessageViewset

router = DefaultRouter()
router.register(r'client', ClientViewset, basename='client')
router.register(r'mailinglist', MailingListViewset, basename='user')
router.register(r'message', MessageViewset, basename='user')
urlpatterns = [
    *router.urls
]