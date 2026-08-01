
def disabled():
    """
    Context manager that disables running validators within its context.

    .. warning::

        This context manager is not thread-safe!

    .. versionadded:: 21.3.0
    .. versionchanged:: 26.1.0 The contextmanager is nestable.
    """
    prev = get_run_validators()
    set_run_validators(False)
    try:
        yield
    finally:
        set_run_validators(prev)

