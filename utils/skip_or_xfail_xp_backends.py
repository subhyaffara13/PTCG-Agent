
def skip_or_xfail_xp_backends(request: pytest.FixtureRequest,
                              skip_or_xfail: Literal['skip', 'xfail']) -> None:
    """
    Helper of the `xp` fixture.
    Skip or xfail based on the ``skip_xp_backends`` or ``xfail_xp_backends`` markers.

    See the "Support for the array API standard" docs page for usage examples.

    Usage
    -----
    ::
        skip_xp_backends = pytest.mark.skip_xp_backends
        xfail_xp_backends = pytest.mark.xfail_xp_backends
        ...

        @skip_xp_backends(backend, *, reason=None)
        @skip_xp_backends(backend, condition, /, *, reason='skip because condition')
        @skip_xp_backends(*, cpu_only=True, exceptions=(), reason=None)
        @skip_xp_backends(*, eager_only=True, exceptions=(), reason=None)
        @skip_xp_backends(*, np_only=True, exceptions=(), reason=None)

        @xfail_xp_backends(backend, *, reason=None)
        @xfail_xp_backends(backend, condition, /, *, reason='xfail because condition')
        @xfail_xp_backends(*, cpu_only=True, exceptions=(), reason=None)
        @xfail_xp_backends(*, eager_only=True, exceptions=(), reason=None)
        @xfail_xp_backends(*, np_only=True, exceptions=(), reason=None)

    Parameters
    ----------
    backend : str, optional
        Backend to skip/xfail, e.g. ``"torch"``.
        Mutually exclusive with ``cpu_only``, ``eager_only``, and ``np_only``.
    cpu_only : bool, optional
        When ``True``, the test is skipped/xfailed on non-CPU devices,
        minus exceptions. Mutually exclusive with ``backend``.
    eager_only : bool, optional
        When ``True``, the test is skipped/xfailed for lazy backends, e.g. those
        with major caveats when invoking ``__array__``, ``__bool__``, ``__float__``,
        or ``__complex__``, minus exceptions. Mutually exclusive with ``backend``.
    np_only : bool, optional
        When ``True``, the test is skipped/xfailed for all backends other
        than the default NumPy backend and the exceptions.
        Mutually exclusive with ``backend``. Implies ``cpu_only`` and ``eager_only``.
    reason : str, optional
        A reason for the skip/xfail. If omitted, a default reason is used.
    exceptions : list[str], optional
        A list of exceptions for use with ``cpu_only``, ``eager_only``, or ``np_only``.
        This should be provided when delegation is implemented for some,
        but not all, non-CPU/non-NumPy backends.
    """
    if f"{skip_or_xfail}_xp_backends" not in request.keywords:
        return

    skip_xfail_reasons = _backends_kwargs_from_request(
        request, skip_or_xfail=skip_or_xfail
    )
    xp = request.param
    if xp.__name__ in skip_xfail_reasons:
        reason = skip_xfail_reasons[xp.__name__]
        assert reason  # Default reason applied above
        skip_or_xfail = getattr(pytest, skip_or_xfail)
        skip_or_xfail(reason=reason)

