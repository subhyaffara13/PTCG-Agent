
def deprecated_call():
    """
    pytest.deprecated_call() seems broken in pytest<3.9.x; concretely, it
    doesn't work on CPython 3.8.0 with pytest==3.3.2 on Ubuntu 18.04 (#2922).

    This is a narrowed reimplementation of the following PR :(
    https://github.com/pytest-dev/pytest/pull/4104
    """
    # TODO: Remove this when testing requires pytest>=3.9.
    pieces = pytest.__version__.split(".")
    pytest_major_minor = (int(pieces[0]), int(pieces[1]))
    if pytest_major_minor < (3, 9):
        return pytest.warns((DeprecationWarning, PendingDeprecationWarning))
    return pytest.deprecated_call()


def deprecated_call(
    *, match: str | re.Pattern[str] | None = ...
) -> WarningsRecorder: ...


def deprecated_call(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T: ...


def deprecated_call(
    func: Callable[..., Any] | None = None, *args: Any, **kwargs: Any
) -> WarningsRecorder | Any:
    """Assert that code produces a ``DeprecationWarning`` or ``PendingDeprecationWarning`` or ``FutureWarning``.

    This function can be used as a context manager::

        >>> import warnings
        >>> def api_call_v2():
        ...     warnings.warn('use v3 of this api', DeprecationWarning)
        ...     return 200

        >>> import pytest
        >>> with pytest.deprecated_call():
        ...    assert api_call_v2() == 200
        >>> with pytest.deprecated_call(match="^use v3 of this api$") as warning_messages:
        ...    assert api_call_v2() == 200

    You may use the keyword argument ``match`` to assert
    that the warning matches a text or regex.

    The return value is a list of :class:`warnings.WarningMessage` objects,
    one for each warning emitted
    (regardless of whether it is an ``expected_warning`` or not).
    """
    __tracebackhide__ = True
    dep_warnings = (DeprecationWarning, PendingDeprecationWarning, FutureWarning)
    if func is None:
        return warns(dep_warnings, *args, **kwargs)

    with warns(dep_warnings):
        return func(*args, **kwargs)

