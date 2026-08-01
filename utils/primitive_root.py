
def primitive_root(p, smallest=True):
    r""" Returns a primitive root of ``p`` or None.

    Explanation
    ===========

    For the definition of primitive root,
    see the explanation of ``is_primitive_root``.

    The primitive root of ``p`` exist only for
    `p = 2, 4, q^e, 2q^e` (``q`` is an odd prime).
    Now, if we know the primitive root of ``q``,
    we can calculate the primitive root of `q^e`,
    and if we know the primitive root of `q^e`,
    we can calculate the primitive root of `2q^e`.
    When there is no need to find the smallest primitive root,
    this property can be used to obtain a fast primitive root.
    On the other hand, when we want the smallest primitive root,
    we naively determine whether it is a primitive root or not.

    Parameters
    ==========

    p : integer, p > 1
    smallest : if True the smallest primitive root is returned or None

    Returns
    =======

    int | None :
        If the primitive root exists, return the primitive root of ``p``.
        If not, return None.

    Raises
    ======

    ValueError
        If `p \le 1` or ``p`` is not an integer.

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import primitive_root
    >>> primitive_root(19)
    2
    >>> primitive_root(21) is None
    True
    >>> primitive_root(50, smallest=False)
    27

    See Also
    ========

    is_primitive_root

    References
    ==========

    .. [1] W. Stein "Elementary Number Theory" (2011), page 44
    .. [2] P. Hackman "Elementary Number Theory" (2009), Chapter C

    """
    p = as_int(p)
    if p <= 1:
        raise ValueError("p should be an integer greater than 1")
    if p <= 4:
        return p - 1
    p_even = p % 2 == 0
    if not p_even:
        q = p  # p is odd
    elif p % 4:
        q = p//2  # p had 1 factor of 2
    else:
        return None  # p had more than one factor of 2
    if isprime(q):
        e = 1
    else:
        m = _perfect_power(q, 3)
        if not m:
            return None
        q, e = m
        if not isprime(q):
            return None
    if not smallest:
        if p_even:
            return next(_primitive_root_prime_power2_iter(q, e))
        return next(_primitive_root_prime_power_iter(q, e))
    if p_even:
        for i in range(3, p, 2):
            if i % q and is_primitive_root(i, p):
                return i
    g = next(_primitive_root_prime_iter(q))
    if e == 1 or pow(g, q - 1, q**2) != 1:
        return g
    for i in range(g + 1, p):
        if i % q and is_primitive_root(i, p):
            return i

