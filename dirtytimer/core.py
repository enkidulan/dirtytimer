import configparser
import importlib
from zope import component
# from .collecting_pluggins.git_repo import GitCollector
from .interfaces import ITimeCollector


from zope.component import getUtility


def get_sections(sections, config):

    for section in sections:
        provider = config[section].pop('provider')
        utility = getUtility(ITimeCollector, provider)(config)
        data = utility.get_activity(config[section])
        yield section, data


def collect_time_stats(config, params=None):

    config = configparser.ConfigParser()
    config.read('config.cfg')

    # providers = (p.split('=') for p in config['base']['collectors'].split())
    # for provider, doten_path in providers:
    #     module, klass = doten_path.rsplit('.', 1)
    #     utility = getattr(importlib.import_module(module), klass)
    #     component.provideUtility(utility(None), ITimeCollector, provider)

    data = dict(get_sections(config['base']['parts'].split(), config))
    print(data)
    # import pdb; pdb.set_trace()
    return data

