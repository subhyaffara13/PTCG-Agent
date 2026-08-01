
def runtestprotocol(
    item: Item, log: bool = True, nextitem: Item | None = None
) -> list[TestReport]:
    hasrequest = hasattr(item, "_request")
    if hasrequest and not item._request:  # type: ignore[attr-defined]
        # This only happens if the item is re-run, as is done by
        # pytest-rerunfailures.
        item._initrequest()  # type: ignore[attr-defined]
    try:
        rep = call_and_report(item, "setup", log)
        reports = [rep]
        if rep.passed:
            setup_only = item.config.getoption("setuponly", False)
            if item.config.getoption("setupshow", False):
                show_test_item(item, add_space=not setup_only)
            if not setup_only:
                reports.append(call_and_report(item, "call", log))
        # If the session is about to fail or stop, teardown everything - this is
        # necessary to correctly report fixture teardown errors (see #11706)
        if item.session.shouldfail or item.session.shouldstop:
            nextitem = None
        reports.append(call_and_report(item, "teardown", log, nextitem=nextitem))
    finally:
        # After all teardown hooks have been called (or an exception was reraised)
        # want funcargs and request info to go away.
        if hasrequest:
            item._request = False  # type: ignore[attr-defined]
            item.funcargs = None  # type: ignore[attr-defined]
    return reports

