from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='dirtytimer',
      version=version,
      description="Time reporting tool for repoting time into various systems based on development and tasks managment activity.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='time reporting',
      author='Maksym Shalenyi (enkidulan)',
      author_email='supamaxy@gmail.com',
      url='',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'setuptools',
          'docopt',
          'arrow',
          'pyyaml',
          'GitPython',
          'PyGithub',
          'jira',
          'zope.interface',
          'zope.component',
      ],
      entry_points="""
      [console_scripts]
      dirtytimer_collect = dirtytimer.cli:collect
      dirtytimer_report = dirtytimer.cli:report
      # -*- Entry points: -*-
      """,
      )
