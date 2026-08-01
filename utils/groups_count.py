
def groups_count(n):
    r""" Number of groups of order `n`.
    In [1]_, ``gnu(n)`` is given, so we follow this notation here as well.

    Parameters
    ==========

    n : Integer
        ``n`` is a positive integer

    Returns
    =======

    int : ``gnu(n)``

    Raises
    ======

    ValueError
        Number of groups of order ``n`` is unknown or not implemented.
        For example, gnu(`2^{11}`) is not yet known.
        On the other hand, gnu(99) is known to be 2,
        but this has not yet been implemented in this function.

    Examples
    ========

    >>> from sympy.combinatorics.group_numbers import groups_count
    >>> groups_count(3) # There is only one cyclic group of order 3
    1
    >>> # There are two groups of order 10: the cyclic group and the dihedral group
    >>> groups_count(10)
    2

    See Also
    ========

    is_cyclic_number
        `n` is cyclic iff gnu(n) = 1

    References
    ==========

    .. [1] John H. Conway, Heiko Dietrich and E.A. O'Brien,
           Counting groups: gnus, moas and other exotica
           The Mathematical Intelligencer 30, 6-15 (2008)
           https://doi.org/10.1007/BF02985731
    .. [2] https://oeis.org/A000001

    """
    n = as_int(n)
    if n <= 0:
        raise ValueError("n must be a positive integer, not %i" % n)
    factors = factorint(n)
    if len(factors) == 1:
        (p, e) = list(factors.items())[0]
        if p == 2:
            A000679 = [1, 1, 2, 5, 14, 51, 267, 2328, 56092, 10494213, 49487367289]
            if e < len(A000679):
                return A000679[e]
        if p == 3:
            A090091 = [1, 1, 2, 5, 15, 67, 504, 9310, 1396077, 5937876645]
            if e < len(A090091):
                return A090091[e]
        if e <= 2: # gnu(p) = 1, gnu(p**2) = 2
            return e
        if e == 3: # gnu(p**3) = 5
            return 5
        if e == 4: # if p is an odd prime, gnu(p**4) = 15
            return 15
        if e == 5: # if p >= 5, gnu(p**5) is expressed by the following equation
            return 61 + 2*p + 2*gcd(p-1, 3) + gcd(p-1, 4)
        if e == 6: # if p >= 6, gnu(p**6) is expressed by the following equation
            return 3*p**2 + 39*p + 344 +\
                  24*gcd(p-1, 3) + 11*gcd(p-1, 4) + 2*gcd(p-1, 5)
        if e == 7: # if p >= 7, gnu(p**7) is expressed by the following equation
            if p == 5:
                return 34297
            return 3*p**5 + 12*p**4 + 44*p**3 + 170*p**2 + 707*p + 2455 +\
                  (4*p**2 + 44*p + 291)*gcd(p-1, 3) + (p**2 + 19*p + 135)*gcd(p-1, 4) + \
                  (3*p + 31)*gcd(p-1, 5) + 4*gcd(p-1, 7) + 5*gcd(p-1, 8) + gcd(p-1, 9)
    if any(e > 1 for e in factors.values()): # n is not squarefree
        # some known values for small n that have more than 1 factor and are not square free (https://oeis.org/A000001)
        small = {12: 5, 18: 5, 20: 5, 24: 15, 28: 4, 36: 14, 40: 14, 44: 4, 45: 2, 48: 52,
                50: 5, 52: 5, 54: 15, 56: 13, 60: 13, 63: 4, 68: 5, 72: 50, 75: 3, 76: 4,
                80: 52, 84: 15, 88: 12, 90: 10, 92: 4}
        if n in small:
            return small[n]
        raise ValueError("Number of groups of order n is unknown or not implemented")
    if len(factors) == 2: # n is squarefree semiprime
        p, q = sorted(factors.keys())
        return 2 if q % p == 1 else 1
    return _holder_formula(set(factors.keys()))

