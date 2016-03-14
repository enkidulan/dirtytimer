import configparser
from itertools import groupby
from operator import itemgetter
from collections import defaultdict

import arrow
from zope.component import getUtility
import yaml

from .interfaces import ITimeCollector


def get_items(day):
    for atype, activities in day.items():
        for activity in activities:
            yield {'type': atype, 'comment': activity.comment, 'task': activity.task}


def get_sections(sections, config):

    for section in sections:
        provider = config[section].pop('provider')
        utility = getUtility(ITimeCollector, provider)(config)
        data = utility.get_activity(config[section])
        yield section, data


def day_report_creator(day):

    day_stats = defaultdict(lambda: defaultdict(dict))

    for task, activity in groupby(get_items(day), itemgetter('task')):
        for atype, records in groupby(activity, itemgetter('type')):
            day_stats[task][atype] = [r['comment'] for r in records]

    return day_stats


def report_creator(data):
    stats = {
        day: day_report_creator(day_stats) for day, day_stats in data.items()
    }
    report = defaultdict(str)
    for day, day_stats in stats.items():
        for task, task_stats in day_stats.items():
            jira_stats = task_stats.get('jira')
            if jira_stats:
                report[day] += 'Where working on task {0} "{1}"'.format(
                    task, " xxxxxx ".join(jira_stats))
            git_stats = task_stats.get('git')
            if git_stats:
                msg = '. In scope of it did' if jira_stats else 'Spent time working on'
                report[day] += msg + ':\n    * {0}'.format(
                    ("\n".join('"    * {0}"'.format(i) for i in git_stats)))
            github_stats = task_stats.get('git')
            if github_stats:
                report[day] += 'Spent time on reviewing PRs:\n    * {0}'.format(
                    ("\n".join('"    * {0}"'.format(i) for i in github_stats)))
            report[day] += '\n'

    return report


def collect_time_stats(config, params=None):

    config = configparser.ConfigParser()
    config.read('config.cfg')

    data = dict(get_sections(config['base']['collectors'].split(), config))
    events_by_day = {}
    for provider, records in data.items():
        for record in records:
            day = arrow.get(record.date).strftime("%Y-%m-%d")
            events_by_day.setdefault(day, {}).setdefault(provider, []).append(record)

    stats = report_creator(events_by_day)

    report = [{
            'day': day,
            'msg': msg,
            'time': '8h',
            'task': 'x'

        } for day, msg in stats.items()]

    with open('report.yml', 'w') as outfile:
        outfile.write(yaml.safe_dump(report, default_flow_style=False))
