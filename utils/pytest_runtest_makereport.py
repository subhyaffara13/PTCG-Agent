
def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> TestReport | None:
    """Called to create a :class:`~pytest.TestReport` for each of
    the setup, call and teardown runtest phases of a test item.

    See :hook:`pytest_runtest_protocol` for a description of the runtest protocol.

    :param item: The item.
    :param call: The :class:`~pytest.CallInfo` for the phase.

    Stops at first non-None result, see :ref:`firstresult`.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """


def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> TestReport:
    return TestReport.from_item_and_call(item, call)


def pytest_runtest_makereport(
    item: Item, call: CallInfo[None]
) -> Generator[None, TestReport, TestReport]:
    rep = yield
    xfailed = item.stash.get(xfailed_key, None)
    if item.config.option.runxfail:
        pass  # don't interfere
    elif call.excinfo and isinstance(call.excinfo.value, xfail.Exception):
        assert call.excinfo.value.msg is not None
        rep.wasxfail = call.excinfo.value.msg
        rep.outcome = "skipped"
    elif not rep.skipped and xfailed:
        if call.excinfo:
            raises = xfailed.raises
            if raises is None or (
                (
                    isinstance(raises, type | tuple)
                    and isinstance(call.excinfo.value, raises)
                )
                or (
                    isinstance(raises, AbstractRaises)
                    and raises.matches(call.excinfo.value)
                )
            ):
                rep.outcome = "skipped"
                rep.wasxfail = xfailed.reason
            else:
                rep.outcome = "failed"
        elif call.when == "call":
            if xfailed.strict:
                rep.outcome = "failed"
                rep.longrepr = "[XPASS(strict)] " + xfailed.reason
            else:
                rep.outcome = "passed"
                rep.wasxfail = xfailed.reason
    return rep


def pytest_runtest_makereport(
    item: Item, call
) -> Generator[None, TestReport, TestReport]:
    rep = yield
    assert rep.when is not None
    empty: dict[str, bool] = {}
    item.stash.setdefault(tmppath_result_key, empty)[rep.when] = rep.passed
    return rep


def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> None:
    if isinstance(item, TestCaseFunction):
        if item._excinfo:
            call.excinfo = item._excinfo.pop(0)
            try:
                del call.result
            except AttributeError:
                pass

    # Convert unittest.SkipTest to pytest.skip.
    # This covers explicit `raise unittest.SkipTest`.
    unittest = sys.modules.get("unittest")
    if unittest and call.excinfo and isinstance(call.excinfo.value, unittest.SkipTest):
        excinfo = call.excinfo
        call2 = CallInfo[None].from_call(lambda: skip(str(excinfo.value)), call.when)
        call.excinfo = call2.excinfo

