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

        # check issues assigned on user and is in targeted statuses, or status was chened in given period

        # TODO: dates seems to be random...
        statuses = ("Code Review", "In Progress")
        subquery_item = '(status CHANGED during ("{after}", "{before}") TO "{status}" and assignee = "{user}")'
        subquery = " or ".join(subquery_item.format(status=s, **params) for s in statuses)
        query = '''
            project={project}
            and (assignee = "{user}" and status in {statuses})
            or {subquery}'''.format(subquery=subquery, statuses=statuses, **params)
        issues = jira.search_issues(query, expand='changelog')

        # import pdb; pdb.set_trace()

        work_records = [
            WorkRecord(
                date=issue.fields.updated,
                comment=issue.fields.summary,
                task=issue.key,
                type=issue.fields.status.name)
            for issue in issues]
        return work_records
