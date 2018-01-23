from datetime import datetime, time
from itertools import combinations

from django.test import TestCase

from workatolist.phonecalls import pricing


class PricingRulesTest(TestCase):
    ''' Test if the rules satisfies the assumptions'''

    @staticmethod
    def _has_overlap(rules):
        is_inside = lambda x, y: (y.start <= x.start < y.end or
                                  y.start < x.end <= y.end)
        for i, j in combinations(rules, 2):
            if is_inside(i, j) or is_inside(j, i):
                return True
        return False

    @staticmethod
    def _is_sorted(rules):
        for i, rule in enumerate(rules[:-1]):
            if rule.start > rules[i+1].start:
                return False
        return True

    @staticmethod
    def _is_continuous(rules):
        for i, rule in enumerate(rules):
            if rules[i-1].end != rule.start:
                return False
        return True

    def test_overlapping(self):
        self.assertFalse(self._has_overlap(pricing.RULES),
                         'The rules shouldn\'t overlap')

    def test_ordering(self):
        self.assertTrue(self._is_sorted(pricing.RULES),
                        'Rules must be ordered by the time they start')

    def test_continuity(self):
        self.assertTrue(self._is_continuous(pricing.RULES),
                        'Should exist rules for all times of the day')


class CalculatePriceTest(TestCase):
    '''Test calculation of the call cost'''

    def setUp(self):
        self.original_rules = pricing.RULES

    def tearDown(self):
        pricing.RULES = self.original_rules

    def test_simple_charge_with_current_rules(self):
        start = datetime(2018, 1, 10, 21, 57, 13)
        end = datetime(2018, 1, 10, 22, 10, 56)

        self.assertEqual(0.54, pricing.calculate_price(start, end),
                         'The calculated price is wrong')

    def test_non_completed_minutes(self):
        pricing.RULES = [pricing.Rule(start=time(hour=0, minute=0, second=0),
                                      end=time(hour=12, minute=0, second=0),
                                      connection_charge=1.00,
                                      duration_charge=10.0),
                         pricing.Rule(start=time(hour=12, minute=0, second=0),
                                      end=time(hour=0, minute=0, second=0),
                                      connection_charge=1.0,
                                      duration_charge=5.0)]

        start = datetime(2018, 1, 10, 11, 59, 1)
        end = datetime(2018, 1, 10, 12, 0, 59)

        self.assertEqual(1.0, pricing.calculate_price(start, end),
                         ('The calculated price should be'
                          ' just the connection charge'))

    def test_call_pass_through_midnight(self):
        pricing.RULES = [pricing.Rule(start=time(4, 30, 0),
                                      end=time(21, 57, 0),
                                      connection_charge=0.36,
                                      duration_charge=0.09),
                         pricing.Rule(start=time(21, 57, 0),
                                      end=time(4, 30, 0),
                                      connection_charge=0.36,
                                      duration_charge=0.01)]

        start = datetime(2018, 1, 10, 23, 57, 0)
        end = datetime(2018, 1, 11, 0, 1, 0)

        self.assertEqual(0.4, pricing.calculate_price(start, end),
                         ('The calculated price is wrong when a call'
                          ' extrapolates the day'))

    def test_call_pass_through_multiple_rules(self):
        pricing.RULES = [pricing.Rule(start=time(0, 0, 0),
                                      end=time(12, 1, 0),
                                      connection_charge=0.6,
                                      duration_charge=0.5),
                         pricing.Rule(start=time(12, 1, 0),
                                      end=time(12, 2, 0),
                                      connection_charge=0.01,
                                      duration_charge=2.2),
                         pricing.Rule(start=time(12, 2, 0),
                                      end=time(0, 0, 0),
                                      connection_charge=0.01,
                                      duration_charge=3.3)]

        start = datetime(2018, 1, 10, 12, 0, 0)
        end = datetime(2018, 1, 10, 12, 3, 22)

        self.assertEqual(6.6, pricing.calculate_price(start, end),
                         ('The calculated price is wrong when a call'
                          ' extrapolates the day'))

