from zope.interface import Interface, Attribute


class ITimeCollector(Interface):
    """ Interface for time collector """

    config = Attribute("Config for TimeCollector Utility")

    def get_activity(start_date, end_date, filters=None):
        """
        Return time etries in following format:

        >>> (Record(date=datatime, comment="activity comment", task="TaskID"),
        ...  ... )

        """
        pass


class ITimeReporter(Interface):

    config = Attribute("Config for TimeReporter Utility")

    def report_time(timeenties):
        """
        Takes time entries in format and reports them into destinatin set in
        config. Entries are in following format:

        >>> (Record(date=datatime, comment="activity comment", task="TaskID"),
        ...  ...)
        """
        pass
