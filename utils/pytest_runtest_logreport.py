
def pytest_runtest_logreport(report: TestReport) -> None:
    """Process the :class:`~pytest.TestReport` produced for each
    of the setup, call and teardown runtest phases of an item.

    See :hook:`pytest_runtest_protocol` for a description of the runtest protocol.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """

