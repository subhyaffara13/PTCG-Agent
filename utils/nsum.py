
def nsum(f, a, b, *, step=1, args=(), kwargs=None,
         log=False, maxterms=int(2**20), tolerances=None):
    r"""Evaluate a convergent finite or infinite series.

    For finite `a` and `b`, this evaluates::

        f(a + np.arange(n)*step).sum()

    where ``n = int((b - a) / step) + 1``, where `f` is smooth, positive, and
    unimodal. The number of terms in the sum may be very large or infinite,
    in which case a partial sum is evaluated directly and the remainder is
    approximated using integration.

    Parameters
    ----------
    f : callable
        The function that evaluates terms to be summed. The signature must be::

            f(x: ndarray, *args) -> ndarray

        where each element of ``x`` is a finite real and ``args`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable
        with ``x``.

        `f` must be an elementwise function: each element ``f(x)[i]``
        must equal ``f(x[i])`` for all indices ``i``. It must not mutate the
        array ``x`` or the arrays in ``args``, and it must return NaN where
        the argument is NaN.

        `f` must represent a smooth, positive, unimodal function of `x` defined at
        *all reals* between `a` and `b`.
    a, b : float array_like
        Real lower and upper limits of summed terms. Must be broadcastable.
        Each element of `a` must be less than the corresponding element in `b`.
    step : float array_like
        Finite, positive, real step between summed terms. Must be broadcastable
        with `a` and `b`. Note that the number of terms included in the sum will
        be ``floor((b - a) / step)`` + 1; adjust `b` accordingly to ensure
        that ``f(b)`` is included if intended.
    args : tuple of array_like, optional
        Additional positional arguments to be passed to `f`. Must be arrays
        broadcastable with `a`, `b`, and `step`. If the callable to be summed
        requires arguments that are not broadcastable with `a`, `b`, and `step`,
        wrap that callable with `f` such that `f` accepts only `x` and
        broadcastable ``*args``. See Examples.
    kwargs : dict of str:array_like, optional
        Additional keyword arguments to be passed to `f`. See `args`.
    log : bool, default: False
        Setting to True indicates that `f` returns the log of the terms
        and that `atol` and `rtol` are expressed as the logs of the absolute
        and relative errors. In this case, the result object will contain the
        log of the sum and error. This is useful for summands for which
        numerical underflow or overflow would lead to inaccuracies.
    maxterms : int, default: 2**20
        The maximum number of terms to evaluate for direct summation.
        Additional function evaluations may be performed for input
        validation and integral evaluation.
    tolerances : dict, optional
        Dictionary with recognized keys ``atol`` for absolute termination tolerance
        (default: 0) and ``rtol`` for relative termination tolerance (default:
        ``eps**0.5``, where ``eps`` is the precision of the result dtype), respectively.
        Values must be non-negative and finite if `log` is False, and must be expressed
        as the log of a non-negative and finite number if `log` is True.

    Returns
    -------
    res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. (The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.)

        success : bool
            ``True`` when the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : Element(s) of `a`, `b`, or `step` are invalid
            - ``-2`` : Numerical integration reached its iteration limit;
              the sum may be divergent.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : The magnitude of the last term of the partial sum exceeds
              the tolerances, so the error estimate exceeds the tolerances.
              Consider increasing `maxterms` or loosening `tolerances`.
              Alternatively, the callable may not be unimodal, or the limits of
              summation may be too far from the function maximum. Consider
              increasing `maxterms` or breaking the sum into pieces.

        sum : float array
            An estimate of the sum.
        error : float array
            An estimate of the absolute error, assuming all terms are non-negative,
            the function is computed exactly, and direct summation is accurate to
            the precision of the result dtype.
        nfev : int array
            The number of points at which `f` was evaluated.

    See Also
    --------
    mpmath.nsum

    Notes
    -----
    The method implemented for infinite summation is related to the integral
    test for convergence of an infinite series: assuming `step` size 1 for
    simplicity of exposition, the sum of a monotone decreasing function is bounded by

    .. math::

        \int_u^\infty f(x) dx \leq \sum_{k=u}^\infty f(k) \leq \int_u^\infty f(x) dx + f(u)

    Let :math:`a` represent  `a`, :math:`n` represent `maxterms`, :math:`\epsilon_a`
    represent `atol`, and :math:`\epsilon_r` represent `rtol`.
    The implementation first evaluates the integral :math:`S_l=\int_a^\infty f(x) dx`
    as a lower bound of the infinite sum. Then, it seeks a value :math:`c > a` such
    that :math:`f(c) < \epsilon_a + S_l \epsilon_r`, if it exists; otherwise,
    let :math:`c = a + n`. Then the infinite sum is approximated as

    .. math::

        \sum_{k=a}^{c-1} f(k) + \int_c^\infty f(x) dx + f(c)/2

    and the reported error is :math:`f(c)/2` plus the error estimate of
    numerical integration. Note that the integral approximations may require
    evaluation of the function at points besides those that appear in the sum,
    so `f` must be a continuous and monotonically decreasing function defined
    for all reals within the integration interval. However, due to the nature
    of the integral approximation, the shape of the function between points
    that appear in the sum has little effect. If there is not a natural
    extension of the function to all reals, consider using linear interpolation,
    which is easy to evaluate and preserves monotonicity.

    The approach described above is generalized for non-unit
    `step` and finite `b` that is too large for direct evaluation of the sum,
    i.e. ``b - a + 1 > maxterms``. It is further generalized to unimodal
    functions by directly summing terms surrounding the maximum.
    This strategy may fail:

    - If the left limit is finite and the maximum is far from it.
    - If the right limit is finite and the maximum is far from it.
    - If both limits are finite and the maximum is far from the origin.

    In these cases, accuracy may be poor, and `nsum` may return status code ``4``.

    Although the callable `f` must be non-negative and unimodal,
    `nsum` can be used to evaluate more general forms of series. For instance, to
    evaluate an alternating series, pass a callable that returns the difference
    between pairs of adjacent terms, and adjust `step` accordingly. See Examples.

    References
    ----------
    .. [1] Wikipedia. "Integral test for convergence."
           https://en.wikipedia.org/wiki/Integral_test_for_convergence

    Examples
    --------
    Compute the infinite sum of the reciprocals of squared integers.

    >>> import numpy as np
    >>> from scipy.integrate import nsum
    >>> res = nsum(lambda k: 1/k**2, 1, np.inf)
    >>> ref = np.pi**2/6  # true value
    >>> res.error  # estimated error
    np.float64(7.448762306416137e-09)
    >>> (res.sum - ref)/ref  # true error
    np.float64(-1.839871898894426e-13)
    >>> res.nfev  # number of points at which callable was evaluated
    np.int32(8561)

    Compute the infinite sums of the reciprocals of integers raised to powers ``p``,
    where ``p`` is an array.

    >>> from scipy import special
    >>> p = np.arange(3, 10)
    >>> res = nsum(lambda k, p: 1/k**p, 1, np.inf, maxterms=1e3, args=(p,))
    >>> ref = special.zeta(p, 1)
    >>> np.allclose(res.sum, ref)
    True

    Evaluate the alternating harmonic series.

    >>> res = nsum(lambda x: 1/x - 1/(x+1), 1, np.inf, step=2)
    >>> res.sum, res.sum - np.log(2)  # result, difference vs analytical sum
    (np.float64(0.6931471805598691), np.float64(-7.616129948928574e-14))

    """ # noqa: E501
    # Potential future work:
    # - improve error estimate of `_direct` sum
    # - add other methods for convergence acceleration (Richardson, epsilon)
    # - support negative monotone increasing functions?
    # - b < a / negative step?
    # - complex-valued function?
    # - check for violations of monotonicity?

    # Function-specific input validation / standardization
    tmp = _nsum_iv(f, a, b, step, args, kwargs, log, maxterms, tolerances)
    f, a, b, step, valid_abstep, args, kwargs, log, maxterms, atol, rtol, xp = tmp

    # Additional elementwise algorithm input validation / standardization
    tmp = eim._initialize(f, (a,), args, kwargs=kwargs, complex_ok=False, xp=xp)
    f, xs, fs, args, shape, dtype, xp = tmp

    # Finish preparing `a`, `b`, and `step` arrays
    a = xs[0]
    b = xp.astype(xp_ravel(xp.broadcast_to(b, shape)), dtype)
    step = xp.astype(xp_ravel(xp.broadcast_to(step, shape)), dtype)
    valid_abstep = xp_ravel(xp.broadcast_to(valid_abstep, shape))
    nterms = xp.floor((b - a) / step)
    finite_terms = xp.isfinite(nterms)
    b[finite_terms] = a[finite_terms] + nterms[finite_terms]*step[finite_terms]

    # Define constants
    eps = xp.finfo(dtype).eps
    zero = xp.asarray(-xp.inf if log else 0, dtype=dtype)[()]
    if rtol is None:
        rtol = 0.5*math.log(eps) if log else eps**0.5
    constants = (dtype, log, eps, zero, rtol, atol, maxterms)

    # Prepare result arrays
    S = xp.empty_like(a)
    E = xp.empty_like(a)
    status = xp.zeros(len(a), dtype=xp.int32)
    nfev = xp.ones(len(a), dtype=xp.int32)  # one function evaluation above

    # Branch for direct sum evaluation / integral approximation / invalid input
    i0 = ~valid_abstep                     # invalid
    i0b = b < a                            # zero
    i1 = (nterms + 1 <= maxterms) & ~i0    # direct sum evaluation
    i2 = xp.isfinite(a) & ~i1 & ~i0        # infinite sum to the right
    i3 = xp.isfinite(b) & ~i2 & ~i1 & ~i0  # infinite sum to the left
    i4 = ~i3 & ~i2 & ~i1 & ~i0             # infinite sum on both sides

    if xp.any(i0):
        S[i0], E[i0] = xp.nan, xp.nan
        status[i0] = -1

        S[i0b], E[i0b] = zero, zero
        status[i0b] = 0

    if xp.any(i1):
        args_direct = [arg[i1] for arg in args]
        tmp = _direct(f, a[i1], b[i1], step[i1], args_direct, constants, xp)
        S[i1], E[i1] = tmp[:-1]
        nfev[i1] += tmp[-1]
        status[i1] = -3 * xp.asarray(~xp.isfinite(S[i1]), dtype=xp.int32)

    if xp.any(i2):
        args_indirect = [arg[i2] for arg in args]
        tmp = _integral_bound(f, a[i2], b[i2], step[i2],
                              args_indirect, constants, xp)
        S[i2], E[i2], status[i2] = tmp[:-1]
        nfev[i2] += tmp[-1]

    if xp.any(i3):
        args_indirect = [arg[i3] for arg in args]
        def _f(x, *args): return f(-x, *args)
        tmp = _integral_bound(_f, -b[i3], -a[i3], step[i3],
                              args_indirect, constants, xp)
        S[i3], E[i3], status[i3] = tmp[:-1]
        nfev[i3] += tmp[-1]

    if xp.any(i4):
        args_indirect = [arg[i4] for arg in args]

        # There are two obvious high-level strategies:
        # - Do two separate half-infinite sums (e.g. from -inf to 0 and 1 to inf)
        # - Make a callable that returns f(x) + f(-x) and do a single half-infinite sum
        # I thought the latter would have about half the overhead, so I went that way.
        # Then there are two ways of ensuring that f(0) doesn't get counted twice.
        # - Evaluate the sum from 1 to inf and add f(0)
        # - Evaluate the sum from 0 to inf and subtract f(0)
        # - Evaluate the sum from 0 to inf, but apply a weight of 0.5 when `x = 0`
        # The last option has more overhead, but is simpler to implement correctly
        # (especially getting the status message right)
        if log:
            def _f(x, *args):
                log_factor = xp.where(x==0, math.log(0.5), 0)
                out = xp.stack([f(x, *args), f(-x, *args)], axis=0)
                return special.logsumexp(out, axis=0) + log_factor

        else:
            def _f(x, *args):
                factor = xp.where(x==0, 0.5, 1)
                return (f(x, *args) + f(-x, *args)) * factor

        zero = xp.zeros_like(a[i4])
        tmp = _integral_bound(_f, zero, b[i4], step[i4], args_indirect, constants, xp)
        S[i4], E[i4], status[i4] = tmp[:-1]
        nfev[i4] += 2*tmp[-1]

    # Return results
    S, E = S.reshape(shape)[()], E.reshape(shape)[()]
    status, nfev = status.reshape(shape)[()], nfev.reshape(shape)[()]
    return _RichResult(sum=S, error=E, status=status, success=status == 0,
                       nfev=nfev)


def nsum(ctx, f, *intervals, **options):
    r"""
    Computes the sum

    .. math :: S = \sum_{k=a}^b f(k)

    where `(a, b)` = *interval*, and where `a = -\infty` and/or
    `b = \infty` are allowed, or more generally

    .. math :: S = \sum_{k_1=a_1}^{b_1} \cdots
                   \sum_{k_n=a_n}^{b_n} f(k_1,\ldots,k_n)

    if multiple intervals are given.

    Two examples of infinite series that can be summed by :func:`~mpmath.nsum`,
    where the first converges rapidly and the second converges slowly,
    are::

        >>> from mpmath import *
        >>> mp.dps = 15; mp.pretty = True
        >>> nsum(lambda n: 1/fac(n), [0, inf])
        2.71828182845905
        >>> nsum(lambda n: 1/n**2, [1, inf])
        1.64493406684823

    When appropriate, :func:`~mpmath.nsum` applies convergence acceleration to
    accurately estimate the sums of slowly convergent series. If the series is
    finite, :func:`~mpmath.nsum` currently does not attempt to perform any
    extrapolation, and simply calls :func:`~mpmath.fsum`.

    Multidimensional infinite series are reduced to a single-dimensional
    series over expanding hypercubes; if both infinite and finite dimensions
    are present, the finite ranges are moved innermost. For more advanced
    control over the summation order, use nested calls to :func:`~mpmath.nsum`,
    or manually rewrite the sum as a single-dimensional series.

    **Options**

    *tol*
        Desired maximum final error. Defaults roughly to the
        epsilon of the working precision.

    *method*
        Which summation algorithm to use (described below).
        Default: ``'richardson+shanks'``.

    *maxterms*
        Cancel after at most this many terms. Default: 10*dps.

    *steps*
        An iterable giving the number of terms to add between
        each extrapolation attempt. The default sequence is
        [10, 20, 30, 40, ...]. For example, if you know that
        approximately 100 terms will be required, efficiency might be
        improved by setting this to [100, 10]. Then the first
        extrapolation will be performed after 100 terms, the second
        after 110, etc.

    *verbose*
        Print details about progress.

    *ignore*
        If enabled, any term that raises ``ArithmeticError``
        or ``ValueError`` (e.g. through division by zero) is replaced
        by a zero. This is convenient for lattice sums with
        a singular term near the origin.

    **Methods**

    Unfortunately, an algorithm that can efficiently sum any infinite
    series does not exist. :func:`~mpmath.nsum` implements several different
    algorithms that each work well in different cases. The *method*
    keyword argument selects a method.

    The default method is ``'r+s'``, i.e. both Richardson extrapolation
    and Shanks transformation is attempted. A slower method that
    handles more cases is ``'r+s+e'``. For very high precision
    summation, or if the summation needs to be fast (for example if
    multiple sums need to be evaluated), it is a good idea to
    investigate which one method works best and only use that.

    ``'richardson'`` / ``'r'``:
        Uses Richardson extrapolation. Provides useful extrapolation
        when `f(k) \sim P(k)/Q(k)` or when `f(k) \sim (-1)^k P(k)/Q(k)`
        for polynomials `P` and `Q`. See :func:`~mpmath.richardson` for
        additional information.

    ``'shanks'`` / ``'s'``:
        Uses Shanks transformation. Typically provides useful
        extrapolation when `f(k) \sim c^k` or when successive terms
        alternate signs. Is able to sum some divergent series.
        See :func:`~mpmath.shanks` for additional information.

    ``'levin'`` / ``'l'``:
        Uses the Levin transformation. It performs better than the Shanks
        transformation for logarithmic convergent or alternating divergent
        series. The ``'levin_variant'``-keyword selects the variant. Valid
        choices are "u", "t", "v" and "all" whereby "all" uses all three
        u,t and v simultanously (This is good for performance comparison in
        conjunction with "verbose=True"). Instead of the Levin transform one can
        also use the Sidi-S transform by selecting the method ``'sidi'``.
        See :func:`~mpmath.levin` for additional details.

    ``'alternating'`` / ``'a'``:
        This is the convergence acceleration of alternating series developped
        by Cohen, Villegras and Zagier.
        See :func:`~mpmath.cohen_alt` for additional details.

    ``'euler-maclaurin'`` / ``'e'``:
        Uses the Euler-Maclaurin summation formula to approximate
        the remainder sum by an integral. This requires high-order
        numerical derivatives and numerical integration. The advantage
        of this algorithm is that it works regardless of the
        decay rate of `f`, as long as `f` is sufficiently smooth.
        See :func:`~mpmath.sumem` for additional information.

    ``'direct'`` / ``'d'``:
        Does not perform any extrapolation. This can be used
        (and should only be used for) rapidly convergent series.
        The summation automatically stops when the terms
        decrease below the target tolerance.

    **Basic examples**

    A finite sum::

        >>> nsum(lambda k: 1/k, [1, 6])
        2.45

    Summation of a series going to negative infinity and a doubly
    infinite series::

        >>> nsum(lambda k: 1/k**2, [-inf, -1])
        1.64493406684823
        >>> nsum(lambda k: 1/(1+k**2), [-inf, inf])
        3.15334809493716

    :func:`~mpmath.nsum` handles sums of complex numbers::

        >>> nsum(lambda k: (0.5+0.25j)**k, [0, inf])
        (1.6 + 0.8j)

    The following sum converges very rapidly, so it is most
    efficient to sum it by disabling convergence acceleration::

        >>> mp.dps = 1000
        >>> a = nsum(lambda k: -(-1)**k * k**2 / fac(2*k), [1, inf],
        ...     method='direct')
        >>> b = (cos(1)+sin(1))/4
        >>> abs(a-b) < mpf('1e-998')
        True

    **Examples with Richardson extrapolation**

    Richardson extrapolation works well for sums over rational
    functions, as well as their alternating counterparts::

        >>> mp.dps = 50
        >>> nsum(lambda k: 1 / k**3, [1, inf],
        ...     method='richardson')
        1.2020569031595942853997381615114499907649862923405
        >>> zeta(3)
        1.2020569031595942853997381615114499907649862923405

        >>> nsum(lambda n: (n + 3)/(n**3 + n**2), [1, inf],
        ...     method='richardson')
        2.9348022005446793094172454999380755676568497036204
        >>> pi**2/2-2
        2.9348022005446793094172454999380755676568497036204

        >>> nsum(lambda k: (-1)**k / k**3, [1, inf],
        ...     method='richardson')
        -0.90154267736969571404980362113358749307373971925537
        >>> -3*zeta(3)/4
        -0.90154267736969571404980362113358749307373971925538

    **Examples with Shanks transformation**

    The Shanks transformation works well for geometric series
    and typically provides excellent acceleration for Taylor
    series near the border of their disk of convergence.
    Here we apply it to a series for `\log(2)`, which can be
    seen as the Taylor series for `\log(1+x)` with `x = 1`::

        >>> nsum(lambda k: -(-1)**k/k, [1, inf],
        ...     method='shanks')
        0.69314718055994530941723212145817656807550013436025
        >>> log(2)
        0.69314718055994530941723212145817656807550013436025

    Here we apply it to a slowly convergent geometric series::

        >>> nsum(lambda k: mpf('0.995')**k, [0, inf],
        ...     method='shanks')
        200.0

    Finally, Shanks' method works very well for alternating series
    where `f(k) = (-1)^k g(k)`, and often does so regardless of
    the exact decay rate of `g(k)`::

        >>> mp.dps = 15
        >>> nsum(lambda k: (-1)**(k+1) / k**1.5, [1, inf],
        ...     method='shanks')
        0.765147024625408
        >>> (2-sqrt(2))*zeta(1.5)/2
        0.765147024625408

    The following slowly convergent alternating series has no known
    closed-form value. Evaluating the sum a second time at higher
    precision indicates that the value is probably correct::

        >>> nsum(lambda k: (-1)**k / log(k), [2, inf],
        ...     method='shanks')
        0.924299897222939
        >>> mp.dps = 30
        >>> nsum(lambda k: (-1)**k / log(k), [2, inf],
        ...     method='shanks')
        0.92429989722293885595957018136

    **Examples with Levin transformation**

    The following example calculates Euler's constant as the constant term in
    the Laurent expansion of zeta(s) at s=1. This sum converges extremly slow
    because of the logarithmic convergence behaviour of the Dirichlet series
    for zeta.

      >>> mp.dps = 30
      >>> z = mp.mpf(10) ** (-10)
      >>> a = mp.nsum(lambda n: n**(-(1+z)), [1, mp.inf], method = "levin") - 1 / z
      >>> print(mp.chop(a - mp.euler, tol = 1e-10))
      0.0

    Now we sum the zeta function outside its range of convergence
    (attention: This does not work at the negative integers!):

      >>> mp.dps = 15
      >>> w = mp.nsum(lambda n: n ** (2 + 3j), [1, mp.inf], method = "levin", levin_variant = "v")
      >>> print(mp.chop(w - mp.zeta(-2-3j)))
      0.0

    The next example resummates an asymptotic series expansion of an integral
    related to the exponential integral.

      >>> mp.dps = 15
      >>> z = mp.mpf(10)
      >>> # exact = mp.quad(lambda x: mp.exp(-x)/(1+x/z),[0,mp.inf])
      >>> exact = z * mp.exp(z) * mp.expint(1,z) # this is the symbolic expression for the integral
      >>> w = mp.nsum(lambda n: (-1) ** n * mp.fac(n) * z ** (-n), [0, mp.inf], method = "sidi", levin_variant = "t")
      >>> print(mp.chop(w - exact))
      0.0

    Following highly divergent asymptotic expansion needs some care. Firstly we
    need copious amount of working precision. Secondly the stepsize must not be
    chosen to large, otherwise nsum may miss the point where the Levin transform
    converges and reach the point where only numerical garbage is produced due to
    numerical cancellation.

      >>> mp.dps = 15
      >>> z = mp.mpf(2)
      >>> # exact = mp.quad(lambda x: mp.exp( -x * x / 2 - z * x ** 4), [0,mp.inf]) * 2 / mp.sqrt(2 * mp.pi)
      >>> exact = mp.exp(mp.one / (32 * z)) * mp.besselk(mp.one / 4, mp.one / (32 * z)) / (4 * mp.sqrt(z * mp.pi)) # this is the symbolic expression for the integral
      >>> w = mp.nsum(lambda n: (-z)**n * mp.fac(4 * n) / (mp.fac(n) * mp.fac(2 * n) * (4 ** n)),
      ...   [0, mp.inf], method = "levin", levin_variant = "t", workprec = 8*mp.prec, steps = [2] + [1 for x in xrange(1000)])
      >>> print(mp.chop(w - exact))
      0.0

    The hypergeoemtric function can also be summed outside its range of convergence:

      >>> mp.dps = 15
      >>> z = 2 + 1j
      >>> exact = mp.hyp2f1(2 / mp.mpf(3), 4 / mp.mpf(3), 1 / mp.mpf(3), z)
      >>> f = lambda n: mp.rf(2 / mp.mpf(3), n) * mp.rf(4 / mp.mpf(3), n) * z**n / (mp.rf(1 / mp.mpf(3), n) * mp.fac(n))
      >>> v = mp.nsum(f, [0, mp.inf], method = "levin", steps = [10 for x in xrange(1000)])
      >>> print(mp.chop(exact-v))
      0.0

    **Examples with Cohen's alternating series resummation**

      The next example sums the alternating zeta function:

      >>> v = mp.nsum(lambda n: (-1)**(n-1) / n, [1, mp.inf], method = "a")
      >>> print(mp.chop(v - mp.log(2)))
      0.0

      The derivate of the alternating zeta function outside its range of
      convergence:

      >>> v = mp.nsum(lambda n: (-1)**n * mp.log(n) * n, [1, mp.inf], method = "a")
      >>> print(mp.chop(v - mp.diff(lambda s: mp.altzeta(s), -1)))
      0.0

    **Examples with Euler-Maclaurin summation**

    The sum in the following example has the wrong rate of convergence
    for either Richardson or Shanks to be effective.

        >>> f = lambda k: log(k)/k**2.5
        >>> mp.dps = 15
        >>> nsum(f, [1, inf], method='euler-maclaurin')
        0.38734195032621
        >>> -diff(zeta, 2.5)
        0.38734195032621

    Increasing ``steps`` improves speed at higher precision::

        >>> mp.dps = 50
        >>> nsum(f, [1, inf], method='euler-maclaurin', steps=[250])
        0.38734195032620997271199237593105101319948228874688
        >>> -diff(zeta, 2.5)
        0.38734195032620997271199237593105101319948228874688

    **Divergent series**

    The Shanks transformation is able to sum some *divergent*
    series. In particular, it is often able to sum Taylor series
    beyond their radius of convergence (this is due to a relation
    between the Shanks transformation and Pade approximations;
    see :func:`~mpmath.pade` for an alternative way to evaluate divergent
    Taylor series). Furthermore the Levin-transform examples above
    contain some divergent series resummation.

    Here we apply it to `\log(1+x)` far outside the region of
    convergence::

        >>> mp.dps = 50
        >>> nsum(lambda k: -(-9)**k/k, [1, inf],
        ...     method='shanks')
        2.3025850929940456840179914546843642076011014886288
        >>> log(10)
        2.3025850929940456840179914546843642076011014886288

    A particular type of divergent series that can be summed
    using the Shanks transformation is geometric series.
    The result is the same as using the closed-form formula
    for an infinite geometric series::

        >>> mp.dps = 15
        >>> for n in range(-8, 8):
        ...     if n == 1:
        ...         continue
        ...     print("%s %s %s" % (mpf(n), mpf(1)/(1-n),
        ...         nsum(lambda k: n**k, [0, inf], method='shanks')))
        ...
        -8.0 0.111111111111111 0.111111111111111
        -7.0 0.125 0.125
        -6.0 0.142857142857143 0.142857142857143
        -5.0 0.166666666666667 0.166666666666667
        -4.0 0.2 0.2
        -3.0 0.25 0.25
        -2.0 0.333333333333333 0.333333333333333
        -1.0 0.5 0.5
        0.0 1.0 1.0
        2.0 -1.0 -1.0
        3.0 -0.5 -0.5
        4.0 -0.333333333333333 -0.333333333333333
        5.0 -0.25 -0.25
        6.0 -0.2 -0.2
        7.0 -0.166666666666667 -0.166666666666667

    **Multidimensional sums**

    Any combination of finite and infinite ranges is allowed for the
    summation indices::

        >>> mp.dps = 15
        >>> nsum(lambda x,y: x+y, [2,3], [4,5])
        28.0
        >>> nsum(lambda x,y: x/2**y, [1,3], [1,inf])
        6.0
        >>> nsum(lambda x,y: y/2**x, [1,inf], [1,3])
        6.0
        >>> nsum(lambda x,y,z: z/(2**x*2**y), [1,inf], [1,inf], [3,4])
        7.0
        >>> nsum(lambda x,y,z: y/(2**x*2**z), [1,inf], [3,4], [1,inf])
        7.0
        >>> nsum(lambda x,y,z: x/(2**z*2**y), [3,4], [1,inf], [1,inf])
        7.0

    Some nice examples of double series with analytic solutions or
    reductions to single-dimensional series (see [1])::

        >>> nsum(lambda m, n: 1/2**(m*n), [1,inf], [1,inf])
        1.60669515241529
        >>> nsum(lambda n: 1/(2**n-1), [1,inf])
        1.60669515241529

        >>> nsum(lambda i,j: (-1)**(i+j)/(i**2+j**2), [1,inf], [1,inf])
        0.278070510848213
        >>> pi*(pi-3*ln2)/12
        0.278070510848213

        >>> nsum(lambda i,j: (-1)**(i+j)/(i+j)**2, [1,inf], [1,inf])
        0.129319852864168
        >>> altzeta(2) - altzeta(1)
        0.129319852864168

        >>> nsum(lambda i,j: (-1)**(i+j)/(i+j)**3, [1,inf], [1,inf])
        0.0790756439455825
        >>> altzeta(3) - altzeta(2)
        0.0790756439455825

        >>> nsum(lambda m,n: m**2*n/(3**m*(n*3**m+m*3**n)),
        ...     [1,inf], [1,inf])
        0.28125
        >>> mpf(9)/32
        0.28125

        >>> nsum(lambda i,j: fac(i-1)*fac(j-1)/fac(i+j),
        ...     [1,inf], [1,inf], workprec=400)
        1.64493406684823
        >>> zeta(2)
        1.64493406684823

    A hard example of a multidimensional sum is the Madelung constant
    in three dimensions (see [2]). The defining sum converges very
    slowly and only conditionally, so :func:`~mpmath.nsum` is lucky to
    obtain an accurate value through convergence acceleration. The
    second evaluation below uses a much more efficient, rapidly
    convergent 2D sum::

        >>> nsum(lambda x,y,z: (-1)**(x+y+z)/(x*x+y*y+z*z)**0.5,
        ...     [-inf,inf], [-inf,inf], [-inf,inf], ignore=True)
        -1.74756459463318
        >>> nsum(lambda x,y: -12*pi*sech(0.5*pi * \
        ...     sqrt((2*x+1)**2+(2*y+1)**2))**2, [0,inf], [0,inf])
        -1.74756459463318

    Another example of a lattice sum in 2D::

        >>> nsum(lambda x,y: (-1)**(x+y) / (x**2+y**2), [-inf,inf],
        ...     [-inf,inf], ignore=True)
        -2.1775860903036
        >>> -pi*ln2
        -2.1775860903036

    An example of an Eisenstein series::

        >>> nsum(lambda m,n: (m+n*1j)**(-4), [-inf,inf], [-inf,inf],
        ...     ignore=True)
        (3.1512120021539 + 0.0j)

    **References**

    1. [Weisstein]_ http://mathworld.wolfram.com/DoubleSeries.html,
    2. [Weisstein]_ http://mathworld.wolfram.com/MadelungConstants.html

    """
    infinite, g = standardize(ctx, f, intervals, options)
    if not infinite:
        return +g()

    def update(partial_sums, indices):
        if partial_sums:
            psum = partial_sums[-1]
        else:
            psum = ctx.zero
        for k in indices:
            psum = psum + g(ctx.mpf(k))
            partial_sums.append(psum)

    prec = ctx.prec

    def emfun(point, tol):
        workprec = ctx.prec
        ctx.prec = prec + 10
        v = ctx.sumem(g, [point, ctx.inf], tol, error=1)
        ctx.prec = workprec
        return v

    return +ctx.adaptive_extrapolation(update, emfun, options)

