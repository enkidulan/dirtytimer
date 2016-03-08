from git import Repo
from zope.interface import implementer
import tempfile
import re

from ..interfaces import ITimeCollector
from ..types import WorkRecord


@implementer(ITimeCollector)
class GitCollector():

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
        task_re = re.compile(params['task_pattern'])

        def get_task(msg):
            match = task_re.search(msg)
            if match:
                match.group()

        with tempfile.TemporaryDirectory() as folder:
            repo = Repo.clone_from(params['git_url'], folder)
            commits = repo.iter_commits(
                all=True,
                author=params['author'],
                after=params['after'],
                before=params['before'])
            work_records = [
                WorkRecord(
                    date=commit.committed_date,
                    comment=task_re.sub('', commit.message).replace('\n', ''),
                    type=commit.type,
                    task=get_task(commit.message))
                for commit in commits]
            return work_records
