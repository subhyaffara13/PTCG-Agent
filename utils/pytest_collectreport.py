
def pytest_collectreport(report: CollectReport) -> None:
    """Collector finished collecting.

    :param report:
        The collect report.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given collector, only
    conftest files in the collector's directory and its parent directories are
    consulted.
    """

