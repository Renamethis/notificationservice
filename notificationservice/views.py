from .serializers import ClientSerializer, MalingListSerializer, MessageSerializer
from .models import Client, MailingList, Message
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import JsonResponse

# Client model Viewset
class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

# MailingList model Viewset
class MailingListViewset(viewsets.ModelViewSet):
    queryset = MailingList.objects.all()
    serializer_class = MalingListSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    # Endpoint which retuns message statistics for one mailing list
    @action(detail=True, methods=['get'], url_path="statistics", url_name="partial_statistics")
    def partial_statistics(self, request, pk):
        return JsonResponse(self.__get_message_statistics(pk), safe=False)

    # Endpoint which retuns main message statistics for each mailing list 
    @action(detail=False, methods=['get'], url_name="statistics")
    def statistics(self, pk=None):
        response = []
        for object in self.queryset:
            response.append({
                'id':object.id,
                'statistics':self.__get_message_statistics(object.id)
            })
        return JsonResponse(response, safe=False)

    # Return message statistics for certain mailing list
    def __get_message_statistics(self, id):
            messages = Message.objects.filter(listId=id)
            result = (messages.values('status')
                .annotate(dcount=Count('status'))
                .order_by()
            )
            return list(result.values('status', 'dcount'))

        

# Message model Viewset
class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']