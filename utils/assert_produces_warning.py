
def assert_produces_warning(
    expected_warning: type[Warning] | bool | tuple[type[Warning], ...] | None = Warning,
    filter_level: Literal[
        "error", "ignore", "always", "default", "module", "once"
    ] = "always",
    check_stacklevel: bool = True,
    raise_on_extra_warnings: bool = True,
    match: str | tuple[str | None, ...] | None = None,
    must_find_all_warnings: bool = True,
) -> Generator[list[warnings.WarningMessage]]:
    """
    Context manager for running code expected to either raise a specific warning,
    multiple specific warnings, or not raise any warnings. Verifies that the code
    raises the expected warning(s), and that it does not raise any other unexpected
    warnings. It is basically a wrapper around ``warnings.catch_warnings``.

    Parameters
    ----------
    expected_warning : {Warning, False, tuple[Warning, ...], None}, default Warning
        The type of Exception raised. ``exception.Warning`` is the base
        class for all warnings. To raise multiple types of exceptions,
        pass them as a tuple. To check that no warning is returned,
        specify ``False`` or ``None``.
    filter_level : str or None, default "always"
        Specifies whether warnings are ignored, displayed, or turned
        into errors.
        Valid values are:

        * "error" - turns matching warnings into exceptions
        * "ignore" - discard the warning
        * "always" - always emit a warning
        * "default" - print the warning the first time it is generated
          from each location
        * "module" - print the warning the first time it is generated
          from each module
        * "once" - print the warning the first time it is generated

    check_stacklevel : bool, default True
        If True, displays the line that called the function containing
        the warning to show were the function is called. Otherwise, the
        line that implements the function is displayed.
    raise_on_extra_warnings : bool, default True
        Whether extra warnings not of the type `expected_warning` should
        cause the test to fail.
    match : {str, tuple[str, ...]}, optional
        Match warning message. If it's a tuple, it has to be the size of
        `expected_warning`. If additionally `must_find_all_warnings` is
        True, each expected warning's message gets matched with a respective
        match. Otherwise, multiple values get treated as an alternative.
    must_find_all_warnings : bool, default True
        If True and `expected_warning` is a tuple, each expected warning
        type must get encountered. Otherwise, even one expected warning
        results in success.

    Examples
    --------
    >>> import warnings
    >>> with assert_produces_warning():
    ...     warnings.warn(UserWarning())
    >>> with assert_produces_warning(False):
    ...     warnings.warn(RuntimeWarning())
    Traceback (most recent call last):
        ...
    AssertionError: Caused unexpected warning(s): ['RuntimeWarning'].
    >>> with assert_produces_warning(UserWarning):
    ...     warnings.warn(RuntimeWarning())
    Traceback (most recent call last):
        ...
    AssertionError: Did not see expected warning of class 'UserWarning'.

    ..warn:: This is *not* thread-safe.
    """
    __tracebackhide__ = True

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter(filter_level)
        try:
            yield w
        finally:
            if expected_warning:
                if isinstance(expected_warning, tuple) and must_find_all_warnings:
                    match = (
                        match
                        if isinstance(match, tuple)
                        else (match,) * len(expected_warning)
                    )
                    for warning_type, warning_match in zip(
                        expected_warning, match, strict=True
                    ):
                        _assert_caught_expected_warnings(
                            caught_warnings=w,
                            expected_warning=warning_type,
                            match=warning_match,
                            check_stacklevel=check_stacklevel,
                        )
                else:
                    expected_warning = cast(
                        Union[type[Warning], tuple[type[Warning], ...]],
                        expected_warning,
                    )
                    match = (
                        "|".join(m for m in match if m)
                        if isinstance(match, tuple)
                        else match
                    )
                    _assert_caught_expected_warnings(
                        caught_warnings=w,
                        expected_warning=expected_warning,
                        match=match,
                        check_stacklevel=check_stacklevel,
                    )
            if raise_on_extra_warnings:
                _assert_caught_no_extra_warnings(
                    caught_warnings=w,
                    expected_warning=expected_warning,
                )

