
def pytest_runtest_logstart(nodeid: str, location: tuple[str, int | None, str]) -> None:
    """Called at the start of running the runtest protocol for a single item.

    See :hook:`pytest_runtest_protocol` for a description of the runtest protocol.

    :param nodeid: Full node ID of the item.
    :param location: A tuple of ``(filename, lineno, testname)``
        where ``filename`` is a file path relative to ``config.rootpath``
        and ``lineno`` is 0-based.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """

