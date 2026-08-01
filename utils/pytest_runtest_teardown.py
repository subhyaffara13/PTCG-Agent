
def pytest_runtest_teardown(item: Item, nextitem: Item | None) -> None:
    """Called to perform the teardown phase for a test item.

    The default implementation runs the finalizers and calls ``teardown()``
    on ``item`` and all of its parents (which need to be torn down). This
    includes running the teardown phase of fixtures required by the item (if
    they go out of scope).

    :param item:
        The item.
    :param nextitem:
        The scheduled-to-be-next test item (None if no further test item is
        scheduled). This argument is used to perform exact teardowns, i.e.
        calling just enough finalizers so that nextitem only needs to call
        setup functions.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """


def pytest_runtest_teardown(item: Item, nextitem: Item | None) -> None:
    _update_current_test_var(item, "teardown")
    item.session._setupstate.teardown_exact(nextitem)
    _update_current_test_var(item, None)


def pytest_runtest_teardown(item: Item) -> None:
    collect_thread_exception(item.config)


def pytest_runtest_teardown(item: Item) -> None:
    collect_unraisable(item.config)

