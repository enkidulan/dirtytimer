from zope.component import getUtilitiesFor
from .interfaces import ITimeCollector


def collect_time_stats(start_date, end_date, config):
    collectors = (klas(config) for _, klas in getUtilitiesFor(ITimeCollector))
    data = [c.get_activity(start_date, end_date) for c in collectors]
    return data
