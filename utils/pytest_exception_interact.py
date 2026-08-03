from typing import Any

def pytest_exception_interact() -> None:
    """Cancel any traceback dumping due to an interactive exception being
    raised."""
    import faulthandler

    faulthandler.cancel_dump_traceback_later()


def pytest_exception_interact(
    node: Item | Collector,
    call: CallInfo[Any],
    report: CollectReport | TestReport,
) -> None:
    """Called when an exception was raised which can potentially be
    interactively handled.

    May be called during collection (see :hook:`pytest_make_collect_report`),
    in which case ``report`` is a :class:`~pytest.CollectReport`.

    May be called during runtest of an item (see :hook:`pytest_runtest_protocol`),
    in which case ``report`` is a :class:`~pytest.TestReport`.

    This hook is not called if the exception that was raised is an internal
    exception like ``skip.Exception``.

    :param node:
        The item or collector.
    :param call:
        The call information. Contains the exception.
    :param report:
        The collection or test report.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given node, only conftest
    files in parent directories of the node are consulted.
    """

