
def _sqrt_mod_prime_power(a, p, k):
    """
    Find the solutions to ``x**2 = a mod p**k`` when ``a % p != 0``.
    If no solution exists, return ``None``.
    Solutions are returned in an ascending list.

    Parameters
    ==========

    a : integer
    p : prime number
    k : positive integer

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _sqrt_mod_prime_power
    >>> _sqrt_mod_prime_power(11, 43, 1)
    [21, 22]

    References
    ==========

    .. [1] P. Hackman "Elementary Number Theory" (2009), page 160
    .. [2] http://www.numbertheory.org/php/squareroot.html
    .. [3] [Gathen99]_
    """
    pk = p**k
    a = a % pk

    if p == 2:
        # see Ref.[2]
        if a % 8 != 1:
            return None
        # Trivial
        if k <= 3:
            return list(range(1, pk, 2))
        r = 1
        # r is one of the solutions to x**2 - a = 0 (mod 2**3).
        # Hensel lift them to solutions of x**2 - a = 0 (mod 2**k)
        # if r**2 - a = 0 mod 2**nx but not mod 2**(nx+1)
        # then r + 2**(nx - 1) is a root mod 2**(nx+1)
        for nx in range(3, k):
            if ((r**2 - a) >> nx) % 2:
                r += 1 << (nx - 1)
        # r is a solution of x**2 - a = 0 (mod 2**k), and
        # there exist other solutions -r, r+h, -(r+h), and these are all solutions.
        h = 1 << (k - 1)
        return sorted([r, pk - r, (r + h) % pk, -(r + h) % pk])

    # If the Legendre symbol (a/p) is not 1, no solution exists.
    if jacobi(a, p) != 1:
        return None
    if p % 4 == 3:
        res = pow(a, (p + 1) // 4, p)
    elif p % 8 == 5:
        res = pow(a, (p + 3) // 8, p)
        if pow(res, 2, p) != a % p:
            res = res * pow(2, (p - 1) // 4, p) % p
    else:
        res = _sqrt_mod_tonelli_shanks(a, p)
    if k > 1:
        # Hensel lifting with Newton iteration, see Ref.[3] chapter 9
        # with f(x) = x**2 - a; one has f'(a) != 0 (mod p) for p != 2
        px = p
        for _ in range(k.bit_length() - 1):
            px = px**2
            frinv = invert(2*res, px)
            res = (res - (res**2 - a)*frinv) % px
        if k & (k - 1): # If k is not a power of 2
            frinv = invert(2*res, pk)
            res = (res - (res**2 - a)*frinv) % pk
    return sorted([res, pk - res])

