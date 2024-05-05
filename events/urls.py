from django.urls import path
from .views import *

urlpatterns = [
    path('event/<int:pk>/register/', EventViewSet.as_view({'post': 'register_for_event'}), name='event-register'),
]