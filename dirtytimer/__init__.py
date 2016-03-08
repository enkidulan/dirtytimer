from zope import component
from .collecting_pluggins.git_repo import GitCollector
from .collecting_pluggins.jira import JiraCollector
from .collecting_pluggins.github import GithubCollector
from .interfaces import ITimeCollector

component.provideUtility(GitCollector, ITimeCollector, 'git')
component.provideUtility(JiraCollector, ITimeCollector, 'jira')
component.provideUtility(GithubCollector, ITimeCollector, 'github')
