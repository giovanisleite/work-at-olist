from datetime import datetime, timedelta

from django.test import TestCase
from django.db.models import Q
from mixer.backend.django import mixer

from workatolist.phonecalls.models import Call


class CallModelTest(TestCase):
    ''' Tests for Call model'''

    def setUp(self):
        self.starts = [None, datetime.now() - timedelta(hours=1, minutes=2, seconds=3),
                       datetime.now() - timedelta(hours=3)]
        ends = [datetime.now()] * 2 + [None]
        mixer.cycle(3).blend(Call, started_at=(start for start in self.starts),
                             finished_at=(finish for finish in ends))
        Call.objects.filter(Q(started_at__isnull=True) |
                            Q(finished_at__isnull=True)).update(price=None)

    def test_ordering(self):
        first_call = Call.objects.only('started_at').first()
        self.assertEqual(first_call.started_at, self.starts[2])

    def test_duration(self):
        call = Call.objects.filter(started_at__isnull=False, finished_at__isnull=False).first()
        self.assertEqual(call.duration, '1h2m3s')

    def test_calculated_price(self):
        with_price = Call.objects.filter(price__isnull=False)
        without_price = Call.objects.filter(price__isnull=True)

        self.assertEqual(with_price.count(), 1)
        self.assertEqual(without_price.count(), 2)
