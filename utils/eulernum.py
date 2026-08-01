
def eulernum(ctx, n, exact=False):
    n = int(n)
    if exact:
        return int(ctx._eulernum(n))
    if n < 100:
        return ctx.mpf(ctx._eulernum(n))
    if n % 2:
        return ctx.zero
    return ctx.ldexp(ctx.eulerpoly(n,0.5), n)


def eulernum(m, _cache={0:MPZ_ONE}):
    r"""
    Computes the Euler numbers `E(n)`, which can be defined as
    coefficients of the Taylor expansion of `1/cosh x`:

    .. math ::

        \frac{1}{\cosh x} = \sum_{n=0}^\infty \frac{E_n}{n!} x^n

    Example::

        >>> [int(eulernum(n)) for n in range(11)]
        [1, 0, -1, 0, 5, 0, -61, 0, 1385, 0, -50521]
        >>> [int(eulernum(n)) for n in range(11)]   # test cache
        [1, 0, -1, 0, 5, 0, -61, 0, 1385, 0, -50521]

    """
    # for odd m > 1, the Euler numbers are zero
    if m & 1:
        return MPZ_ZERO
    f = _cache.get(m)
    if f:
        return f
    MAX = MAX_EULER_CACHE
    n = m
    a = [MPZ(_) for _ in [0,0,1,0,0,0]]
    for  n in range(1, m+1):
        for j in range(n+1, -1, -2):
            a[j+1] = (j-1)*a[j] + (j+1)*a[j+2]
        a.append(0)
        suma = 0
        for k in range(n+1, -1, -2):
            suma += a[k+1]
            if n <= MAX:
                _cache[n] = ((-1)**(n//2))*(suma // 2**n)
        if n == m:
            return ((-1)**(n//2))*suma // 2**n

