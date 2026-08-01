
def _sqrt_mod_tonelli_shanks(a, p):
    """
    Returns the square root in the case of ``p`` prime with ``p == 1 (mod 8)``

    Assume that the root exists.

    Parameters
    ==========

    a : int
    p : int
        prime number. should be ``p % 8 == 1``

    Returns
    =======

    int : Generally, there are two roots, but only one is returned.
          Which one is returned is random.

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _sqrt_mod_tonelli_shanks
    >>> _sqrt_mod_tonelli_shanks(2, 17) in [6, 11]
    True

    References
    ==========

    .. [1] Carl Pomerance, Richard Crandall, Prime Numbers: A Computational Perspective,
           2nd Edition (2005), page 101, ISBN:978-0387252827

    """
    s = bit_scan1(p - 1)
    t = p >> s
    # find a non-quadratic residue
    if p % 12 == 5:
        # Legendre symbol (3/p) == -1 if p % 12 in [5, 7]
        d = 3
    elif p % 5 in [2, 3]:
        # Legendre symbol (5/p) == -1 if p % 5 in [2, 3]
        d = 5
    else:
        while 1:
            d = randint(6, p - 1)
            if jacobi(d, p) == -1:
                break
    #assert legendre_symbol(d, p) == -1
    A = pow(a, t, p)
    D = pow(d, t, p)
    m = 0
    for i in range(s):
        adm = A*pow(D, m, p) % p
        adm = pow(adm, 2**(s - 1 - i), p)
        if adm % p == p - 1:
            m += 2**i
    #assert A*pow(D, m, p) % p == 1
    x = pow(a, (t + 1)//2, p)*pow(D, m//2, p) % p
    return x

