from .core import collect_time_stats


def collect():
    config_file = "config.cfg"
    collect_time_stats(config_file)


def report():
    pass
