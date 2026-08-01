
def raises(err, lamda):
    try:
        lamda()
        return False
    except err:
        return True


def raises(
    expected_exception: type[E] | tuple[type[E], ...],
    *,
    match: str | re.Pattern[str] | None = ...,
    check: Callable[[E], bool] = ...,
) -> RaisesExc[E]: ...


def raises(
    *,
    match: str | re.Pattern[str],
    # If exception_type is not provided, check() must do any typechecks itself.
    check: Callable[[BaseException], bool] = ...,
) -> RaisesExc[BaseException]: ...


def raises(*, check: Callable[[BaseException], bool]) -> RaisesExc[BaseException]: ...


def raises(
    expected_exception: type[E] | tuple[type[E], ...],
    func: Callable[P, object],
    *args: P.args,
    **kwargs: P.kwargs,
) -> ExceptionInfo[E]: ...


def raises(
    expected_exception: type[E] | tuple[type[E], ...] | None = None,
    func: Callable[P, object] | None = None,
    *args: Any,
    **kwargs: Any,
) -> RaisesExc[BaseException] | ExceptionInfo[E]:
    r"""Assert that a code block/function call raises an exception type, or one of its subclasses.

    :param expected_exception:
        The expected exception type, or a tuple if one of multiple possible
        exception types are expected. Note that subclasses of the passed exceptions
        will also match.

        This is not a required parameter, you may opt to only use ``match`` and/or
        ``check`` for verifying the raised exception.

    :kwparam str | re.Pattern[str] | None match:
        If specified, a string containing a regular expression,
        or a regular expression object, that is tested against the string
        representation of the exception and its :pep:`678` `__notes__`
        using :func:`re.search`.

        To match a literal string that may contain :ref:`special characters
        <re-syntax>`, the pattern can first be escaped with :func:`re.escape`.

        (This is only used when ``pytest.raises`` is used as a context manager,
        and passed through to the function otherwise.
        When using ``pytest.raises`` as a function, you can use:
        ``pytest.raises(Exc, func, match="passed on").match("my pattern")``.)

    :kwparam Callable[[BaseException], bool] check:

        .. versionadded:: 8.4

        If specified, a callable that will be called with the exception as a parameter
        after checking the type and the match regex if specified.
        If it returns ``True`` it will be considered a match, if not it will
        be considered a failed match.


    Use ``pytest.raises`` as a context manager, which will capture the exception of the given
    type, or any of its subclasses::

        >>> import pytest
        >>> with pytest.raises(ZeroDivisionError):
        ...    1/0

    If the code block does not raise the expected exception (:class:`ZeroDivisionError` in the example
    above), or no exception at all, the check will fail instead.

    You can also use the keyword argument ``match`` to assert that the
    exception matches a text or regex::

        >>> with pytest.raises(ValueError, match='must be 0 or None'):
        ...     raise ValueError("value must be 0 or None")

        >>> with pytest.raises(ValueError, match=r'must be \d+$'):
        ...     raise ValueError("value must be 42")

    The ``match`` argument searches the formatted exception string, which includes any
    `PEP-678 <https://peps.python.org/pep-0678/>`__ ``__notes__``:

        >>> with pytest.raises(ValueError, match=r"had a note added"):  # doctest: +SKIP
        ...     e = ValueError("value must be 42")
        ...     e.add_note("had a note added")
        ...     raise e

    The ``check`` argument, if provided, must return True when passed the raised exception
    for the match to be successful, otherwise an :exc:`AssertionError` is raised.

        >>> import errno
        >>> with pytest.raises(OSError, check=lambda e: e.errno == errno.EACCES):
        ...     raise OSError(errno.EACCES, "no permission to view")

    The context manager produces an :class:`ExceptionInfo` object which can be used to inspect the
    details of the captured exception::

        >>> with pytest.raises(ValueError) as exc_info:
        ...     raise ValueError("value must be 42")
        >>> assert exc_info.type is ValueError
        >>> assert exc_info.value.args[0] == "value must be 42"

    .. warning::

       Given that ``pytest.raises`` matches subclasses, be wary of using it to match :class:`Exception` like this::

           # Careful, this will catch ANY exception raised.
           with pytest.raises(Exception):
               some_function()

       Because :class:`Exception` is the base class of almost all exceptions, it is easy for this to hide
       real bugs, where the user wrote this expecting a specific exception, but some other exception is being
       raised due to a bug introduced during a refactoring.

       Avoid using ``pytest.raises`` to catch :class:`Exception` unless certain that you really want to catch
       **any** exception raised.

    .. note::

       When using ``pytest.raises`` as a context manager, it's worthwhile to
       note that normal context manager rules apply and that the exception
       raised *must* be the final line in the scope of the context manager.
       Lines of code after that, within the scope of the context manager will
       not be executed. For example::

           >>> value = 15
           >>> with pytest.raises(ValueError) as exc_info:
           ...     if value > 10:
           ...         raise ValueError("value must be <= 10")
           ...     assert exc_info.type is ValueError  # This will not execute.

       Instead, the following approach must be taken (note the difference in
       scope)::

           >>> with pytest.raises(ValueError) as exc_info:
           ...     if value > 10:
           ...         raise ValueError("value must be <= 10")
           ...
           >>> assert exc_info.type is ValueError

    **Expecting exception groups**

    When expecting exceptions wrapped in :exc:`BaseExceptionGroup` or
    :exc:`ExceptionGroup`, you should instead use :class:`pytest.RaisesGroup`.

    **Using with** ``pytest.mark.parametrize``

    When using :ref:`pytest.mark.parametrize ref`
    it is possible to parametrize tests such that
    some runs raise an exception and others do not.

    See :ref:`parametrizing_conditional_raising` for an example.

    .. seealso::

        :ref:`assertraises` for more examples and detailed discussion.

    .. note::
        Similar to caught exception objects in Python, explicitly clearing
        local references to returned ``ExceptionInfo`` objects can
        help the Python interpreter speed up its garbage collection.

        Clearing those references breaks a reference cycle
        (``ExceptionInfo`` --> caught exception --> frame stack raising
        the exception --> current frame stack --> local variables -->
        ``ExceptionInfo``) which makes Python keep all objects referenced
        from that cycle (including all local variables in the current
        frame) alive until the next cyclic garbage collection run.
        More detailed information can be found in the official Python
        documentation for :ref:`the try statement <python:try>`.
    """
    __tracebackhide__ = True

    if func is None and not args:
        if set(kwargs) - {"match", "check", "expected_exception"}:
            msg = "Unexpected keyword arguments passed to pytest.raises: "
            msg += ", ".join(sorted(kwargs))
            msg += "\nUse context-manager form instead?"
            raise TypeError(msg)

        if expected_exception is None:
            return RaisesExc(**kwargs)
        return RaisesExc(expected_exception, **kwargs)

    if not expected_exception:
        raise ValueError(
            f"Expected an exception type or a tuple of exception types, but got `{expected_exception!r}`. "
            f"Raising exceptions is already understood as failing the test, so you don't need "
            f"any special code to say 'this should never raise an exception'."
        )
    if not callable(func):
        raise TypeError(f"{func!r} object (type: {type(func)}) must be callable")
    with RaisesExc(expected_exception) as excinfo:
        func(*args, **kwargs)
    try:
        return excinfo
    finally:
        del excinfo


def raises(err, lamda):  # codespell:ignore lamda
    try:
        lamda()  # codespell:ignore lamda
        return False
    except err:
        return True


def raises(err, lamda):  # codespell:ignore lamda
    try:
        lamda()  # codespell:ignore lamda
        return False
    except err:
        return True

