
def is_primitive_root(a, p):
    r""" Returns True if ``a`` is a primitive root of ``p``.

    Explanation
    ===========

    ``a`` is said to be the primitive root of ``p`` if `\gcd(a, p) = 1` and
    `\phi(p)` is the smallest positive number s.t.

        `a^{\phi(p)} \equiv 1 \pmod{p}`.

    where `\phi(p)` is Euler's totient function.

    The primitive root of ``p`` exist only for
    `p = 2, 4, q^e, 2q^e` (``q`` is an odd prime).
    Hence, if it is not such a ``p``, it returns False.
    To determine the primitive root, we need to know
    the prime factorization of ``q-1``.
    The hardness of the determination depends on this complexity.

    Parameters
    ==========

    a : integer
    p : integer, ``p`` > 1. ``a`` and ``p`` should be relatively prime

    Returns
    =======

    bool : If True, ``a`` is the primitive root of ``p``.

    Raises
    ======

    ValueError
        If `p \le 1` or `\gcd(a, p) \neq 1`.
        If ``a`` or ``p`` is not an integer.

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import totient
    >>> from sympy.ntheory import is_primitive_root, n_order
    >>> is_primitive_root(3, 10)
    True
    >>> is_primitive_root(9, 10)
    False
    >>> n_order(3, 10) == totient(10)
    True
    >>> n_order(9, 10) == totient(10)
    False

    See Also
    ========

    primitive_root

    """
    a, p = as_int(a), as_int(p)
    if p <= 1:
        raise ValueError("p should be an integer greater than 1")
    a = a % p
    if gcd(a, p) != 1:
        raise ValueError("The two numbers should be relatively prime")
    # Primitive root of p exist only for
    # p = 2, 4, q**e, 2*q**e (q is odd prime)
    if p <= 4:
        # The primitive root is only p-1.
        return a == p - 1
    if p % 2:
        q = p  # p is odd
    elif p % 4:
        q = p//2  # p had 1 factor of 2
    else:
        return False  # p had more than one factor of 2
    if isprime(q):
        group_order = q - 1
        factors = factorint(q - 1).keys()
    else:
        m = _perfect_power(q, 3)
        if not m:
            return False
        q, e = m
        if not isprime(q):
            return False
        group_order = q**(e - 1)*(q - 1)
        factors = set(factorint(q - 1).keys())
        factors.add(q)
    return all(pow(a, group_order // prime, p) != 1 for prime in factors)

