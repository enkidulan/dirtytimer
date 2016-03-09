import configparser

import arrow
from zope.component import getUtility

from .interfaces import ITimeCollector


def get_sections(sections, config):

    for section in sections:
        provider = config[section].pop('provider')
        utility = getUtility(ITimeCollector, provider)(config)
        data = utility.get_activity(config[section])
        yield section, data


def collect_time_stats(config, params=None):

    config = configparser.ConfigParser()
    config.read('config.cfg')

    data = dict(get_sections(config['base']['collectors'].split(), config))
    events_by_day = {}
    for provider, records in data.items():
        for record in records:
            day = arrow.get(record.date).strftime("%Y-%m-%d")
            events_by_day.setdefault(day, {}).setdefault(provider, []).append(record)


    from pprint import pprint


    pprint(events_by_day)
    import pdb; pdb.set_trace()
    return data

