
def diffs(ctx, f, x, n=None, **options):
    r"""
    Returns a generator that yields the sequence of derivatives

    .. math ::

        f(x), f'(x), f''(x), \ldots, f^{(k)}(x), \ldots

    With ``method='step'``, :func:`~mpmath.diffs` uses only `O(k)`
    function evaluations to generate the first `k` derivatives,
    rather than the roughly `O(k^2)` evaluations
    required if one calls :func:`~mpmath.diff` `k` separate times.

    With `n < \infty`, the generator stops as soon as the
    `n`-th derivative has been generated. If the exact number of
    needed derivatives is known in advance, this is further
    slightly more efficient.

    Options are the same as for :func:`~mpmath.diff`.

    **Examples**

        >>> from mpmath import *
        >>> mp.dps = 15
        >>> nprint(list(diffs(cos, 1, 5)))
        [0.540302, -0.841471, -0.540302, 0.841471, 0.540302, -0.841471]
        >>> for i, d in zip(range(6), diffs(cos, 1)):
        ...     print("%s %s" % (i, d))
        ...
        0 0.54030230586814
        1 -0.841470984807897
        2 -0.54030230586814
        3 0.841470984807897
        4 0.54030230586814
        5 -0.841470984807897

    """
    if n is None:
        n = ctx.inf
    else:
        n = int(n)
    if options.get('method', 'step') != 'step':
        k = 0
        while k < n + 1:
            yield ctx.diff(f, x, k, **options)
            k += 1
        return
    singular = options.get('singular')
    if singular:
        yield ctx.diff(f, x, 0, singular=True)
    else:
        yield f(ctx.convert(x))
    if n < 1:
        return
    if n == ctx.inf:
        A, B = 1, 2
    else:
        A, B = 1, n+1
    while 1:
        callprec = ctx.prec
        y, norm, workprec = hsteps(ctx, f, x, B, callprec, **options)
        for k in xrange(A, B):
            try:
                ctx.prec = workprec
                d = ctx.difference(y, k) / norm**k
            finally:
                ctx.prec = callprec
            yield +d
            if k >= n:
                return
        A, B = B, int(A*1.4+1)
        B = min(B, n)

