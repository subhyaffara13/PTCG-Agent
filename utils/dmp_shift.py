
def dmp_shift(f, a, u, K):
    """
    Evaluate efficiently Taylor shift ``f(X + A)`` in ``K[X]``.

    Examples
    ========

    >>> from sympy import symbols, ring, ZZ
    >>> x, y = symbols('x y')
    >>> R, _, _ = ring([x, y], ZZ)

    >>> p = x**2*y + 2*x*y + 3*x + 4*y + 5

    >>> R.dmp_shift(R(p), [ZZ(1), ZZ(2)])
    x**2*y + 2*x**2 + 4*x*y + 11*x + 7*y + 22

    >>> p.subs({x: x + 1, y: y + 2}).expand()
    x**2*y + 2*x**2 + 4*x*y + 11*x + 7*y + 22
    """
    if not u:
        return dup_shift(f, a[0], K)

    if dmp_zero_p(f, u):
        return f

    a0, a1 = a[0], a[1:]

    if any(a1):
        f = [ dmp_shift(c, a1, u-1, K) for c in f ]
    else:
        f = list(f)

    if a0:
        n = len(f) - 1

        for i in range(n, 0, -1):
            for j in range(0, i):
                afj = dmp_mul_ground(f[j], a0, u-1, K)
                f[j + 1] = dmp_add(f[j + 1], afj, u-1, K)

    return dmp_strip(f, u)

