#
from zope import component
from .collecting_pluggins.git_repo import GitCollector
from .interfaces import ITimeCollector

component.provideUtility(GitCollector, ITimeCollector)
