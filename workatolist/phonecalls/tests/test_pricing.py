from datetime import datetime, time
from itertools import combinations

from django.test import TestCase

from workatolist.phonecalls import pricing

class PricingRulesTest(TestCase):

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
