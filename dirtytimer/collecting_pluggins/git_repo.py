from git import Repo
from zope.interface import implementer

from ..interfaces import ITimeCollector

from collections import namedtuple

WorkRecord = namedtuple('WorkRecord', ['date', 'comment', 'task'])


@implementer(ITimeCollector)
class GitCollector():

    config = None

    def __init__(self, config):
        self.config = config

    def get_activity(start_date, end_date, filters=None):
        """
        Takes time entries in format and reports them into destinatin set in
        config. Entries are in following format:

        >>> (Record(date=datatime, comment="activity comment", task="TaskID"),
        ...  ...)
        """

        git_url = "https://github.com/enkidulan/slidelint.git"
        repo_dir = "/tmp/repo"
        author = ""
        after = ""
        before = ""

        repo = Repo.clone_from(git_url, repo_dir)
        commits = repo.iter_commits(author=author, after=after, before=before)
        work_records = (
            WorkRecord(
                date=commit.committed_date,
                comment=commit.message,
                task='')
            for commit in commits)
        return work_records
