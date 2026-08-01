
def is_quad_residue(a, p):
    """
    Returns True if ``a`` (mod ``p``) is in the set of squares mod ``p``,
    i.e a % p in set([i**2 % p for i in range(p)]).

    Parameters
    ==========

    a : integer
    p : positive integer

    Returns
    =======

    bool : If True, ``x**2 == a (mod p)`` has solution.

    Raises
    ======

    ValueError
        If ``a``, ``p`` is not integer.
        If ``p`` is not positive.

    Examples
    ========

    >>> from sympy.ntheory import is_quad_residue
    >>> is_quad_residue(21, 100)
    True

    Indeed, ``pow(39, 2, 100)`` would be 21.

    >>> is_quad_residue(21, 120)
    False

    That is, for any integer ``x``, ``pow(x, 2, 120)`` is not 21.

    If ``p`` is an odd
    prime, an iterative method is used to make the determination:

    >>> from sympy.ntheory import is_quad_residue
    >>> sorted(set([i**2 % 7 for i in range(7)]))
    [0, 1, 2, 4]
    >>> [j for j in range(7) if is_quad_residue(j, 7)]
    [0, 1, 2, 4]

    See Also
    ========

    legendre_symbol, jacobi_symbol, sqrt_mod
    """
    a, p = as_int(a), as_int(p)
    if p < 1:
        raise ValueError('p must be > 0')
    a %= p
    if a < 2 or p < 3:
        return True
    # Since we want to compute the Jacobi symbol,
    # we separate p into the odd part and the rest.
    t = bit_scan1(p)
    if t:
        # The existence of a solution to a power of 2 is determined
        # using the logic of `p==2` in `_sqrt_mod_prime_power` and `_sqrt_mod1`.
        a_ = a % (1 << t)
        if a_:
            r = bit_scan1(a_)
            if r % 2 or (a_ >> r) & 6:
                return False
        p >>= t
        a %= p
        if a < 2 or p < 3:
            return True
    # If Jacobi symbol is -1 or p is prime, can be determined by Jacobi symbol only
    j = jacobi(a, p)
    if j == -1 or isprime(p):
        return j == 1
    # Checks if `x**2 = a (mod p)` has a solution
    for px, ex in factorint(p).items():
        if a % px:
            if jacobi(a, px) != 1:
                return False
        else:
            a_ = a % px**ex
            if a_ == 0:
                continue
            a_, r = remove(a_, px)
            if r % 2 or jacobi(a_, px) != 1:
                return False
    return True

