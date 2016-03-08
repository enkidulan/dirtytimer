import re
from jira import JIRA
from zope.interface import implementer

from ..interfaces import ITimeCollector
from ..types import WorkRecord


@implementer(ITimeCollector)
class JiraCollector():

    config = None

    def __init__(self, config):
        self.config = config

    def get_activity(self, params):
        """
        Takes time entries in format and reports them into destinatin set in
        config. Entries are in following format:

        >>> (Record(date=datatime, comment="activity comment", task="TaskID"),
        ...  ...)
        """
        jira = JIRA(
            params['server'], basic_auth=(params['uname'], params['pswd']))
        issues = jira.search_issues(
            'project={project} and assignee = "{user}"'
            ' and updated < "{before}" AND updated > "{after}"'.format(**params))

        work_records = [
            WorkRecord(
                date=issue.fields.updated,
                comment=issue.fields.summary,
                task=issue.key,
                type=issue.fields.status.name)
            for issue in issues]
        return work_records
