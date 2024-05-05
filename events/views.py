from django.utils import timezone
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from events.models import Event
from events.serializers import Events_Serializer
from events.utils import send_registration_email
from user.custom_permossion import IsOrganizerMyEvent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import serializers


class EventListApiPagination(PageNumberPagination):
    page_size = 25
    page_size_query_params = 'page_size'
    max_page_size = 10000000


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = Events_Serializer
    pagination_class = EventListApiPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['place']
    search_fields = ['title', 'description', 'date']
    ordering_fields = ['date']



    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(date__gt=now).order_by('id')

    def register_for_event(self, request, pk=None):
        event = self.get_object()

        if event.organizer == request.user:
            return Response({"error": "You cannot register for your own event."}, status=status.HTTP_400_BAD_REQUEST)

        if event.date <= timezone.now():
            return Response({"error": "Registration is closed for this event."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in event.registered_users.all():
            return Response({"error": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

        event.registered_users.add(request.user)
        event.save()

        send_registration_email(request.user.email, event)

        return Response({"success": "Successfully registered for the event."}, status=status.HTTP_200_OK)


    def get_permissions(self):

        if self.action == 'create':
            return [permissions.IsAuthenticated()]

        elif self.action == 'get_queryset':
            return [permissions.AllowAny()]


        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOrganizerMyEvent()]

        elif self.action == 'register_for_event':
            return [permissions.IsAuthenticated()]

        return super().get_permissions()


    @action(methods=['get'], detail=False)
    def get_my_events(self, request):
        user_id = self.request.user.id
        events = Event.objects.filter(organizer_id=user_id)
        serializer = Events_Serializer(events, many=True)

        return Response(serializer.data)

