from rest_framework import serializers
from user.models import User
from .models import Event

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class Events_Serializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    organizer_email = serializers.SerializerMethodField()
    registered_users_emails = serializers.SerializerMethodField(source='get_registered_users_emails')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'place', 'organizer_email', 'registered_users_emails', 'organizer']

    def get_organizer_email(self, obj):
        return obj.organizer.email

    def get_registered_users_emails(self, obj):
        registered_users = obj.registered_users.all()
        return UserSerializer(registered_users, many=True).data
