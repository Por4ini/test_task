from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from events.models import Event
from events.utils import send_registration_email
from user.models import User


class EventViewSetTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create(email='testuser@mail.com', password='testpassword')
        self.user2 = User.objects.create(email='testuser2@mail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            place='Test Place',
            organizer_id=self.user.id,
            date=timezone.now() + timezone.timedelta(days=7))

    def test_get_queryset(self):

        response = self.client.get('/api/event/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data['count']), 1)
    #
    def test_create_event(self):

        data = {'title': 'New Event',
                'description': 'New Description',
                'date': timezone.now() + timezone.timedelta(days=10),
                "place": 'Test Place',
                "organizer_id": self.user.id }
        response = self.client.post('/api/event/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_update_event(self):

        data = {'title': 'Updated Event'}
        response = self.client.patch(f'/api/event/{self.event.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(id=self.event.id).title, 'Updated Event')


    def test_delete_event(self):

        response = self.client.delete(f'/api/event/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())


    def test_register_for_event(self):
        # Assuming registration is allowed
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/event/{self.event.id}/register/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user2 in self.event.registered_users.all())

    def test_register_for_own_event(self):
        # Attempt to register for own event
        event = Event.objects.create(title='Test Event 2', description='Test Description', date=timezone.now() + timezone.timedelta(days=7), place='test_place' ,organizer=self.user)
        response = self.client.post(f'/api/event/{event.id}/register/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.user in event.registered_users.all())


    def test_get_my_events(self):
        # Assuming the user has organized events
        self.client.force_authenticate(user=self.user)
        Event.objects.create(title='My Event 1', description='My Description', place='test_place', date=timezone.now() + timezone.timedelta(days=7), organizer_id=self.user.id)
        Event.objects.create(title='My Event 2', description='My Description', place='test_place', date=timezone.now() + timezone.timedelta(days=14), organizer_id=self.user.id)
        response = self.client.get('/api/event/get_my_events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_unauthorized_access(self):

        self.client.force_authenticate(user=None)

        # Test accessing restricted endpoints without authentication
        response = self.client.get('/api/event/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post('/api/event/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(f'/api/event/{self.event.id}/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(f'/api/event/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(f'/api/event/{self.event.id}/register/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get('/api/event/get_my_events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class EventFilterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('event-list')
        self.user = User.objects.create(email='testuser@mail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        Event.objects.create(title='Event 1', description='Description 1', date='2024-05-10T14:30:00Z', place='Place 1', organizer_id=self.user.pk)
        Event.objects.create(title='Event 2', description='Description 2', date='2024-05-11T15:30:00Z', place='Place 2', organizer_id=self.user.pk)

    def test_filter_by_place(self):
        response = self.client.get(self.url, {'place': 'Place 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['place'], 'Place 1')

    def test_search_by_title(self):
        response = self.client.get(self.url, {'place': 'Place 2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK),
        self.assertEqual(len(response.data['results']), 1),
        self.assertEqual(response.data['results'][0]['title'], 'Event 2')


class EmailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='testuse2@mail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(title='Test Event', description='Test Description', date='2024-05-10 14:30:00+00:00', place='Test Place', organizer=self.user)

    def test_send_registration_email(self):
        send_registration_email(self.user.email, self.event)

        self.assertEqual(len(mail.outbox), 1)


        self.assertEqual(mail.outbox[0].subject, 'Confirmation of Registration')


        self.assertIn('You have successfully registered for the event', mail.outbox[0].body)
        self.assertIn('Test Event', mail.outbox[0].body)


        self.assertEqual(mail.outbox[0].to[0], self.user.email)