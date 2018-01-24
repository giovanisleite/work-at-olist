from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from mixer.backend.django import mixer

from workatolist.phonecalls.models import Call


class CallViewTest(TestCase):

    def setUp(self):
        self.url = reverse('api:call')
        config = {'id': (n for n in (42, 43)),
                  'started_at': (start for start in (datetime.now()-timedelta(days=3), None)),
                  'finished_at': (finish for finish in (None, datetime.now())),
                  'source': (phone for phone in ('1140228922', None)),
                  'destination': (phone for phone in ('4490456899', None))}
        mixer.cycle(2).blend(Call, **config)

    def test_create_type_start(self):
        data = {'id': 2, 'type': 'start', 'timestamp': '1516757933', 'call_id': 1,
                'source': '1159886999', 'destination': '11998866991'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_type_end(self):
        data = {'id': 1, 'type': 'end', 'timestamp': '1516757933', 'call_id': 2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_type_start(self):
        data = {'id': 36, 'type': 'start', 'timestamp': '1516757933', 'call_id': 43,
                'source': '1159886999', 'destination': '11998866991'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_type_end(self):
        data = {'id': 25, 'type': 'end', 'timestamp': '1516757933', 'call_id': 42}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_type_start(self):
        data = {'id': 171, 'price': 20.43}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data[0], 'The fields don\'t match with those expected')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_create_type_end(self):
        data = {'id': 1, 'type': 'end', 'timestamp': '1516757933', 'call_id': 2, 'price': 20.83}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data[0], 'The fields don\'t match with those expected')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
