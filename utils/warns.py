
def warns(
    expected_warning: type[Warning] | tuple[type[Warning], ...] = ...,
    *,
    match: str | re.Pattern[str] | None = ...,
) -> WarningsChecker: ...


def warns(
    expected_warning: type[Warning] | tuple[type[Warning], ...],
    func: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T: ...


def warns(
    expected_warning: type[Warning] | tuple[type[Warning], ...] = Warning,
    func: Callable[..., object] | None = None,
    *args: Any,
    **kwargs: Any,
) -> WarningsChecker | Any:
    r"""Assert that code raises a particular class of warning.

    Specifically, the parameter ``expected_warning`` can be a warning class or tuple
    of warning classes, and the code inside the ``with`` block must issue at least one
    warning of that class or classes.

    This helper produces a list of :class:`warnings.WarningMessage` objects, one for
    each warning emitted (regardless of whether it is an ``expected_warning`` or not).
    Since pytest 8.0, unmatched warnings are also re-emitted when the context closes.

    This function should be used as a context manager::

        >>> import pytest
        >>> with pytest.warns(RuntimeWarning):
        ...    warnings.warn("my warning", RuntimeWarning)

    The ``match`` keyword argument can be used to assert
    that the warning matches a text or regex::

        >>> with pytest.warns(UserWarning, match='must be 0 or None'):
        ...     warnings.warn("value must be 0 or None", UserWarning)

        >>> with pytest.warns(UserWarning, match=r'must be \d+$'):
        ...     warnings.warn("value must be 42", UserWarning)

        >>> with pytest.warns(UserWarning):  # catch re-emitted warning
        ...     with pytest.warns(UserWarning, match=r'must be \d+$'):
        ...         warnings.warn("this is not here", UserWarning)
        Traceback (most recent call last):
          ...
        Failed: Regex pattern did not match any of the 1 warnings emitted.
         Regex: ...
         Emitted warnings: ...UserWarning...

    **Using with** ``pytest.mark.parametrize``

    When using :ref:`pytest.mark.parametrize ref` it is possible to parametrize tests
    such that some runs raise a warning and others do not.

    This could be achieved in the same way as with exceptions, see
    :ref:`parametrizing_conditional_raising` for an example.

    """
    __tracebackhide__ = True
    if func is None and not args:
        match: str | re.Pattern[str] | None = kwargs.pop("match", None)
        if kwargs:
            argnames = ", ".join(sorted(kwargs))
            raise TypeError(
                f"Unexpected keyword arguments passed to pytest.warns: {argnames}"
                "\nUse context-manager form instead?"
            )
        return WarningsChecker(expected_warning, match_expr=match, _ispytest=True)
    else:
        if not callable(func):
            raise TypeError(f"{func!r} object (type: {type(func)}) must be callable")
        with WarningsChecker(expected_warning, _ispytest=True):
            return func(*args, **kwargs)


def warns(warningcls, *, match='', test_stacklevel=True):
    '''
    Like raises but tests that warnings are emitted.

    >>> from sympy.testing.pytest import warns
    >>> import warnings

    >>> with warns(UserWarning):
    ...     warnings.warn('deprecated', UserWarning, stacklevel=2)

    >>> with warns(UserWarning):
    ...     pass
    Traceback (most recent call last):
    ...
    Failed: DID NOT WARN. No warnings of type UserWarning\
    was emitted. The list of emitted warnings is: [].

    ``test_stacklevel`` makes it check that the ``stacklevel`` parameter to
    ``warn()`` is set so that the warning shows the user line of code (the
    code under the warns() context manager). Set this to False if this is
    ambiguous or if the context manager does not test the direct user code
    that emits the warning.

    If the warning is a ``SymPyDeprecationWarning``, this additionally tests
    that the ``active_deprecations_target`` is a real target in the
    ``active-deprecations.md`` file.

    '''
    # Absorbs all warnings in warnrec
    with warnings.catch_warnings(record=True) as warnrec:
        # Any warning other than the one we are looking for is an error
        warnings.simplefilter("error")
        warnings.filterwarnings("always", category=warningcls)
        # Now run the test
        yield warnrec

    # Raise if expected warning not found
    if not any(issubclass(w.category, warningcls) for w in warnrec):
        msg = ('Failed: DID NOT WARN.'
               ' No warnings of type %s was emitted.'
               ' The list of emitted warnings is: %s.'
               ) % (warningcls, [w.message for w in warnrec])
        raise Failed(msg)

    # We don't include the match in the filter above because it would then
    # fall to the error filter, so we instead manually check that it matches
    # here
    for w in warnrec:
        # Should always be true due to the filters above
        assert issubclass(w.category, warningcls)
        if not re.compile(match, re.IGNORECASE).match(str(w.message)):
            raise Failed(f"Failed: WRONG MESSAGE. A warning with of the correct category ({warningcls.__name__}) was issued, but it did not match the given match regex ({match!r})")

    if test_stacklevel:
        for f in inspect.stack():
            thisfile = f.filename
            file = os.path.split(thisfile)[1]
            if file.startswith('test_'):
                break
            elif file == 'doctest.py':
                # skip the stacklevel testing in the doctests of this
                # function
                return
        else:
            raise RuntimeError("Could not find the file for the given warning to test the stacklevel")
        for w in warnrec:
            if w.filename != thisfile:
                msg = f'''\
Failed: Warning has the wrong stacklevel. The warning stacklevel needs to be
set so that the line of code shown in the warning message is user code that
calls the deprecated code (the current stacklevel is showing code from
{w.filename} (line {w.lineno}), expected {thisfile})'''.replace('\n', ' ')
                raise Failed(msg)

    if warningcls == SymPyDeprecationWarning:
        this_file = pathlib.Path(__file__)
        active_deprecations_file = (this_file.parent.parent.parent / 'doc' /
                                    'src' / 'explanation' /
                                    'active-deprecations.md')
        if not active_deprecations_file.exists():
            # We can only test that the active_deprecations_target works if we are
            # in the git repo.
            return
        targets = []
        for w in warnrec:
            targets.append(w.message.active_deprecations_target)
        text = pathlib.Path(active_deprecations_file).read_text(encoding="utf-8")
        for target in targets:
            if f'({target})=' not in text:
                raise Failed(f"The active deprecations target {target!r} does not appear to be a valid target in the active-deprecations.md file ({active_deprecations_file}).")

