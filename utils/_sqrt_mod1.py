
def _sqrt_mod1(a, p, n):
    """
    Find solution to ``x**2 == a mod p**n`` when ``a % p == 0``.
    If no solution exists, return ``None``.

    Parameters
    ==========

    a : integer
    p : prime number, p must divide a
    n : positive integer

    References
    ==========

    .. [1] http://www.numbertheory.org/php/squareroot.html
    """
    pn = p**n
    a = a % pn
    if a == 0:
        # case gcd(a, p**k) = p**n
        return range(0, pn, p**((n + 1) // 2))
    # case gcd(a, p**k) = p**r, r < n
    a, r = remove(a, p)
    if r % 2 == 1:
        return None
    res = _sqrt_mod_prime_power(a, p, n - r)
    if res is None:
        return None
    m = r // 2
    return (x for rx in res for x in range(rx*p**m, pn, p**(n - m)))

