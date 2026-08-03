import sys

def pytest_runtest_call(item: Item) -> None:
    """Called to run the test for test item (the call phase).

    The default implementation calls ``item.runtest()``.

    :param item:
        The item.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """


def pytest_runtest_call(item: Item) -> None:
    _update_current_test_var(item, "call")
    try:
        del sys.last_type
        del sys.last_value
        del sys.last_traceback
        if sys.version_info >= (3, 12, 0):
            del sys.last_exc  # type:ignore[attr-defined]
    except AttributeError:
        pass
    try:
        item.runtest()
    except Exception as e:
        # Store trace info to allow postmortem debugging
        sys.last_type = type(e)
        sys.last_value = e
        if sys.version_info >= (3, 12, 0):
            sys.last_exc = e  # type:ignore[attr-defined]
        assert e.__traceback__ is not None
        # Skip *this* frame
        sys.last_traceback = e.__traceback__.tb_next
        raise


def pytest_runtest_call(item: Item) -> Generator[None]:
    xfailed = item.stash.get(xfailed_key, None)
    if xfailed is None:
        item.stash[xfailed_key] = xfailed = evaluate_xfail_marks(item)

    if xfailed and not item.config.option.runxfail and not xfailed.run:
        xfail("[NOTRUN] " + xfailed.reason)

    try:
        return (yield)
    finally:
        # The test run may have added an xfail mark dynamically.
        xfailed = item.stash.get(xfailed_key, None)
        if xfailed is None:
            item.stash[xfailed_key] = xfailed = evaluate_xfail_marks(item)


def pytest_runtest_call(item: Item) -> None:
    collect_thread_exception(item.config)


def pytest_runtest_call(item: Item) -> None:
    collect_unraisable(item.config)

