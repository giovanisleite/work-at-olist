from collections import namedtuple
from datetime import datetime, time, timedelta
from operator import attrgetter
from itertools import cycle

Rule = namedtuple('Rule',
                  'start end connection_charge duration_charge')

RULES = sorted(
    [Rule(start=time(hour=6, minute=0, second=0),
          end=time(hour=22, minute=0, second=0),
          connection_charge=0.36,
          duration_charge=0.09),

     Rule(start=time(hour=22, minute=0, second=0),
          end=time(hour=6, minute=0, second=0),
          connection_charge=0.36,
          duration_charge=0.00)],

    key=attrgetter('start')
)


def calculate_price(call_start, call_end):
    ''' Calculate the call cost '''

    rules = cycle(RULES)
    cost = 0
    call_interval_found = False

    while not call_interval_found:
        rule = next(rules)
        if rule.start < rule.end:
            call_interval_found = rule.start <= call_start.time() < rule.end
        else:
            call_interval_found = rule.start <= call_start.time()
    cost += rule.connection_charge

    non_calculated_start = call_start

    while non_calculated_start < call_end:
        duration = _duration_over_interval(non_calculated_start,
                                           call_end,
                                           rule)
        cost += duration.total_seconds()//60 * rule.duration_charge
        non_calculated_start += duration
        rule = next(rules)

    return float(f'{cost:0.2f}')


def _duration_over_interval(call_start, call_end, rule):
    ''' Calculate the overlap between the call (datetime) and the rule interval (time) '''

    rule_start = datetime.combine(call_start.date(), rule.start)
    rule_end = datetime.combine(call_start.date(), rule.end)
    if rule_start > rule_end:
        rule_end += timedelta(days=1)

    if rule_start <= call_end < rule_end:
        return call_end - call_start

    return rule_end - call_start
