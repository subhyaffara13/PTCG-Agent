
def factorialk(n, k, exact=False, extend="zero"):
    """
    Multifactorial of n of order k, n(!!...!).

    This is the multifactorial of n skipping k values.  For example,

      factorialk(17, 4) = 17!!!! = 17 * 13 * 9 * 5 * 1

    In particular, for any integer ``n``, we have

      factorialk(n, 1) = factorial(n)

      factorialk(n, 2) = factorial2(n)

    Parameters
    ----------
    n : int or float or complex (or array_like thereof)
        Input values for multifactorial. Non-integer values require
        ``extend='complex'``. By default, the return value for ``n < 0`` is 0.
    k : int or float or complex (or array_like thereof)
        Order of multifactorial. Non-integer values require ``extend='complex'``.
    exact : bool, optional
        If ``exact`` is set to True, calculate the answer exactly using
        integer arithmetic, otherwise use an approximation (faster,
        but yields floats instead of integers)
        Default is False.
    extend : str, optional
        One of ``'zero'`` or ``'complex'``; this determines how values ``n<0`` are
        handled - by default they are 0, but it is possible to opt into the complex
        extension of the multifactorial. This enables passing complex values,
        not only to ``n`` but also to ``k``.

        .. warning::

           Using the ``'complex'`` extension also changes the values of the
           multifactorial at integers ``n != 1 (mod k)`` by a factor depending
           on both ``k`` and ``n % k``, see below or [1].

    Returns
    -------
    nf : int or float or complex or ndarray
        Multifactorial (order ``k``) of ``n``, as integer, float or complex (depending
        on ``exact`` and ``extend``). Array inputs are returned as arrays.

    Notes
    -----
    While less straight-forward than for the double-factorial, it's possible to
    calculate a general approximation formula of n!(k) by studying ``n`` for a given
    remainder ``r < k`` (thus ``n = m * k + r``, resp. ``r = n % k``), which can be
    put together into something valid for all integer values ``n >= 0`` & ``k > 0``::

      n!(k) = k ** ((n - r)/k) * gamma(n/k + 1) / gamma(r/k + 1) * max(r, 1)

    This is the basis of the approximation when ``exact=False``.

    In principle, any fixed choice of ``r`` (ignoring its relation ``r = n%k``
    to ``n``) would provide a suitable analytic continuation from integer ``n``
    to complex ``z`` (not only satisfying the functional equation but also
    being logarithmically convex, c.f. Bohr-Mollerup theorem) -- in fact, the
    choice of ``r`` above only changes the function by a constant factor. The
    final constraint that determines the canonical continuation is ``f(1) = 1``,
    which forces ``r = 1`` (see also [1]).::

      z!(k) = k ** ((z - 1)/k) * gamma(z/k + 1) / gamma(1/k + 1)

    References
    ----------
    .. [1] Complex extension to multifactorial
            https://en.wikipedia.org/wiki/Double_factorial#Alternative_extension_of_the_multifactorial

    Examples
    --------
    >>> from scipy.special import factorialk
    >>> factorialk(5, k=1, exact=True)
    120
    >>> factorialk(5, k=3, exact=True)
    10
    >>> factorialk([5, 7, 9], k=3, exact=True)
    array([ 10,  28, 162])
    >>> factorialk([5, 7, 9], k=3, exact=False)
    array([ 10.,  28., 162.])
    """
    return _factorialx_wrapper("factorialk", n, k=k, exact=exact, extend=extend)

