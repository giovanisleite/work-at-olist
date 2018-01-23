from datetime import datetime, timedelta

from django.test import TestCase
from mixer.backend.django import mixer

from workatolist.phonecalls.models import Call


class CallModelTest(TestCase):
    ''' Tests for Call model'''

    def setUp(self):
        self.starts = [None, datetime.now() - timedelta(hours=1, minutes=2, seconds=3),
                       datetime.now() - timedelta(hours=3)]
        ends = [datetime.now()] * 2 + [None]
        mixer.cycle(3).blend(Call, started_at=(start for start in self.starts),
                             finished_at=(end for end in ends), price=(None for _ in range(3)))

    def test_ordering(self):
        first_call = Call.objects.only('started_at').first()
        self.assertEqual(first_call.started_at, self.starts[2])

    def test_duration(self):
        call = Call.objects.filter(started_at__isnull=False, finished_at__isnull=False).first()
        self.assertEqual(call.duration, '1h2m3s')
