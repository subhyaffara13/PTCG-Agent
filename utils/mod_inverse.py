
def mod_inverse(a, m):
    r"""
    Return the number $c$ such that, $a \times c = 1 \pmod{m}$
    where $c$ has the same sign as $m$. If no such value exists,
    a ValueError is raised.

    Examples
    ========

    >>> from sympy import mod_inverse, S

    Suppose we wish to find multiplicative inverse $x$ of
    3 modulo 11. This is the same as finding $x$ such
    that $3x = 1 \pmod{11}$. One value of x that satisfies
    this congruence is 4. Because $3 \times 4 = 12$ and $12 = 1 \pmod{11}$.
    This is the value returned by ``mod_inverse``:

    >>> mod_inverse(3, 11)
    4
    >>> mod_inverse(-3, 11)
    7

    When there is a common factor between the numerators of
    `a` and `m` the inverse does not exist:

    >>> mod_inverse(2, 4)
    Traceback (most recent call last):
    ...
    ValueError: inverse of 2 mod 4 does not exist

    >>> mod_inverse(S(2)/7, S(5)/2)
    7/2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
    .. [2] https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
    c = None
    try:
        a, m = as_int(a), as_int(m)
        if m != 1 and m != -1:
            x, _, g = igcdex(a, m)
            if g == 1:
                c = x % m
    except ValueError:
        a, m = sympify(a), sympify(m)
        if not (a.is_number and m.is_number):
            raise TypeError(
                filldedent(
                    """
                Expected numbers for arguments; symbolic `mod_inverse`
                is not implemented
                but symbolic expressions can be handled with the
                similar function,
                sympy.polys.polytools.invert"""
                )
            )
        big = m > 1
        if big not in (S.true, S.false):
            raise ValueError("m > 1 did not evaluate; try to simplify %s" % m)
        elif big:
            c = 1 / a
    if c is None:
        raise ValueError("inverse of %s (mod %s) does not exist" % (a, m))
    return c

