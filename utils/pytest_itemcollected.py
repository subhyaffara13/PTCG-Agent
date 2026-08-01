
def pytest_itemcollected(item):
    """
    Check FPU precision mode was not changed during test collection.

    The clumsy way we do it here is mainly necessary because numpy
    still uses yield tests, which can execute code at test collection
    time.
    """
    global _old_fpu_mode

    mode = get_fpu_mode()

    if _old_fpu_mode is None:
        _old_fpu_mode = mode
    elif mode != _old_fpu_mode:
        _collect_results[item] = (_old_fpu_mode, mode)
        _old_fpu_mode = mode

    # mark f2py tests as thread unsafe
    if Path(item.fspath).parent == Path(__file__).parent / 'f2py' / 'tests':
        item.add_marker(pytest.mark.thread_unsafe(
            reason="f2py tests are thread-unsafe"))


def pytest_itemcollected(item: Item) -> None:
    """We just collected a test item.

    :param item:
        The item.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """

