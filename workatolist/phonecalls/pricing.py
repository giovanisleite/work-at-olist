from operator import attrgetter
from datetime import datetime, time, timedelta
from itertools import cycle
from collections import namedtuple

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
