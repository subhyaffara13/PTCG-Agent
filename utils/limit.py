
def limit(e, z, z0, dir="+"):
    """Computes the limit of ``e(z)`` at the point ``z0``.

    Parameters
    ==========

    e : expression, the limit of which is to be taken

    z : symbol representing the variable in the limit.
        Other symbols are treated as constants. Multivariate limits
        are not supported.

    z0 : the value toward which ``z`` tends. Can be any expression,
        including ``oo`` and ``-oo``.

    dir : string, optional (default: "+")
        The limit is bi-directional if ``dir="+-"``, from the right
        (z->z0+) if ``dir="+"``, and from the left (z->z0-) if
        ``dir="-"``. For infinite ``z0`` (``oo`` or ``-oo``), the ``dir``
        argument is determined from the direction of the infinity
        (i.e., ``dir="-"`` for ``oo``).

    Examples
    ========

    >>> from sympy import limit, sin, oo
    >>> from sympy.abc import x
    >>> limit(sin(x)/x, x, 0)
    1
    >>> limit(1/x, x, 0) # default dir='+'
    oo
    >>> limit(1/x, x, 0, dir="-")
    -oo
    >>> limit(1/x, x, 0, dir='+-')
    zoo
    >>> limit(1/x, x, oo)
    0

    Notes
    =====

    First we try some heuristics for easy and frequent cases like "x", "1/x",
    "x**2" and similar, so that it's fast. For all other cases, we use the
    Gruntz algorithm (see the gruntz() function).

    See Also
    ========

     limit_seq : returns the limit of a sequence.
    """

    return Limit(e, z, z0, dir).doit(deep=False)


def limit(ctx, f, x, direction=1, exp=False, **kwargs):
    r"""
    Computes an estimate of the limit

    .. math ::

        \lim_{t \to x} f(t)

    where `x` may be finite or infinite.

    For finite `x`, :func:`~mpmath.limit` evaluates `f(x + d/n)` for
    consecutive integer values of `n`, where the approach direction
    `d` may be specified using the *direction* keyword argument.
    For infinite `x`, :func:`~mpmath.limit` evaluates values of
    `f(\mathrm{sign}(x) \cdot n)`.

    If the approach to the limit is not sufficiently fast to give
    an accurate estimate directly, :func:`~mpmath.limit` attempts to find
    the limit using Richardson extrapolation or the Shanks
    transformation. You can select between these methods using
    the *method* keyword (see documentation of :func:`~mpmath.nsum` for
    more information).

    **Options**

    The following options are available with essentially the
    same meaning as for :func:`~mpmath.nsum`: *tol*, *method*, *maxterms*,
    *steps*, *verbose*.

    If the option *exp=True* is set, `f` will be
    sampled at exponentially spaced points `n = 2^1, 2^2, 2^3, \ldots`
    instead of the linearly spaced points `n = 1, 2, 3, \ldots`.
    This can sometimes improve the rate of convergence so that
    :func:`~mpmath.limit` may return a more accurate answer (and faster).
    However, do note that this can only be used if `f`
    supports fast and accurate evaluation for arguments that
    are extremely close to the limit point (or if infinite,
    very large arguments).

    **Examples**

    A basic evaluation of a removable singularity::

        >>> from mpmath import *
        >>> mp.dps = 30; mp.pretty = True
        >>> limit(lambda x: (x-sin(x))/x**3, 0)
        0.166666666666666666666666666667

    Computing the exponential function using its limit definition::

        >>> limit(lambda n: (1+3/n)**n, inf)
        20.0855369231876677409285296546
        >>> exp(3)
        20.0855369231876677409285296546

    A limit for `\pi`::

        >>> f = lambda n: 2**(4*n+1)*fac(n)**4/(2*n+1)/fac(2*n)**2
        >>> limit(f, inf)
        3.14159265358979323846264338328

    Calculating the coefficient in Stirling's formula::

        >>> limit(lambda n: fac(n) / (sqrt(n)*(n/e)**n), inf)
        2.50662827463100050241576528481
        >>> sqrt(2*pi)
        2.50662827463100050241576528481

    Evaluating Euler's constant `\gamma` using the limit representation

    .. math ::

        \gamma = \lim_{n \rightarrow \infty } \left[ \left(
        \sum_{k=1}^n \frac{1}{k} \right) - \log(n) \right]

    (which converges notoriously slowly)::

        >>> f = lambda n: sum([mpf(1)/k for k in range(1,int(n)+1)]) - log(n)
        >>> limit(f, inf)
        0.577215664901532860606512090082
        >>> +euler
        0.577215664901532860606512090082

    With default settings, the following limit converges too slowly
    to be evaluated accurately. Changing to exponential sampling
    however gives a perfect result::

        >>> f = lambda x: sqrt(x**3+x**2)/(sqrt(x**3)+x)
        >>> limit(f, inf)
        0.992831158558330281129249686491
        >>> limit(f, inf, exp=True)
        1.0

    """

    if ctx.isinf(x):
        direction = ctx.sign(x)
        g = lambda k: f(ctx.mpf(k+1)*direction)
    else:
        direction *= ctx.one
        g = lambda k: f(x + direction/(k+1))
    if exp:
        h = g
        g = lambda k: h(2**k)

    def update(values, indices):
        for k in indices:
            values.append(g(k+1))

    # XXX: steps used by nsum don't work well
    if not 'steps' in kwargs:
        kwargs['steps'] = [10]

    return +ctx.adaptive_extrapolation(update, None, kwargs)

