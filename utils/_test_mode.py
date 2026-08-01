
def _test_mode(group_names: set[str] | None = None) -> Generator[None, None, None]:
    """
    Forces ``is_symm_mem_enabled_for_group()`` to return ``True`` and the ops
    defined in the ``symm_mem`` namespace to use fallback implementations.

    The context manager is not thread safe.
    """
    global _is_test_mode
    global _mocked_group_names
    prev = _is_test_mode
    prev_group_names = _mocked_group_names
    try:
        _is_test_mode = True
        _mocked_group_names = group_names
        yield
    finally:
        _is_test_mode = prev
        _mocked_group_names = prev_group_names

