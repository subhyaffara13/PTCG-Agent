
def cornacchia(a:int, b:int, m:int) -> set[tuple[int, int]]:
    r"""
    Solves `ax^2 + by^2 = m` where `\gcd(a, b) = 1 = gcd(a, m)` and `a, b > 0`.

    Explanation
    ===========

    Uses the algorithm due to Cornacchia. The method only finds primitive
    solutions, i.e. ones with `\gcd(x, y) = 1`. So this method cannot be used to
    find the solutions of `x^2 + y^2 = 20` since the only solution to former is
    `(x, y) = (4, 2)` and it is not primitive. When `a = b`, only the
    solutions with `x \leq y` are found. For more details, see the References.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import cornacchia
    >>> cornacchia(2, 3, 35) # equation 2x**2 + 3y**2 = 35
    {(2, 3), (4, 1)}
    >>> cornacchia(1, 1, 25) # equation x**2 + y**2 = 25
    {(4, 3)}

    References
    ===========

    .. [1] A. Nitaj, "L'algorithme de Cornacchia"
    .. [2] Solving the diophantine equation ax**2 + by**2 = m by Cornacchia's
        method, [online], Available:
        http://www.numbertheory.org/php/cornacchia.html

    See Also
    ========

    sympy.utilities.iterables.signed_permutations
    """
    # Assume gcd(a, b) = gcd(a, m) = 1 and a, b > 0 but no error checking
    sols = set()

    if a + b > m:
        # xy = 0 must hold if there exists a solution
        if a == 1:
            # y = 0
            s, _exact = iroot(m // a, 2)
            if _exact:
                sols.add((int(s), 0))
            if a == b:
                # only keep one solution
                return sols
        if m % b == 0:
            # x = 0
            s, _exact = iroot(m // b, 2)
            if _exact:
                sols.add((0, int(s)))
        return sols

    # the original cornacchia
    for t in sqrt_mod_iter(-b*invert(a, m), m):
        if t < m // 2:
            continue
        u, r = m, t
        while (m1 := m - a*r**2) <= 0:
            u, r = r, u % r
        m1, _r = divmod(m1, b)
        if _r:
            continue
        s, _exact = iroot(m1, 2)
        if _exact:
            if a == b and r < s:
                r, s = s, r
            sols.add((int(r), int(s)))
    return sols

