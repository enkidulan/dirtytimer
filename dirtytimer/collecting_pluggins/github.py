from functools import lru_cache

import arrow
from github import Github
from zope.interface import implementer

from ..interfaces import ITimeCollector
from ..types import WorkRecord


@implementer(ITimeCollector)
class GithubCollector():

    config = None

    def __init__(self, config):
        self.config = config

    @lru_cache(maxsize=1024)
    def get_pull_title(self, pull_url):
        _, pull_num = pull_url.rsplit('/', 1)
        return self.repo.get_pull(int(pull_num)).title

    def get_activity(self, params):
        """
        Takes time entries in format and reports them into destinatin set in
        config. Entries are in following format:

        >>> (Record(date=datatime, comment="activity comment", task="TaskID"),
        ...  ...)
        """
        github = Github(params['uname'], params['pswd'])
        self.repo = github.get_repo(params['repo_name'])

        work_records = []

        comments = self.repo.get_pulls_review_comments(
            sort='updated', direction='asc', since=arrow.get(params['after']).datetime)
        for comment in comments:

            if comment.user.login != params['login']:
                continue

            work_records.append(
                WorkRecord(
                    date=comment.updated_at,
                    comment=comment.body,
                    task=self.get_pull_title(comment._rawData['pull_request_url']),
                    type=None))

        return work_records
