
def quadratic_congruence(a, b, c, n):
    r"""
    Find the solutions to `a x^2 + b x + c \equiv 0 \pmod{n}`.

    Parameters
    ==========

    a : int
    b : int
    c : int
    n : int
        A positive integer.

    Returns
    =======

    list[int] :
        A sorted list of solutions. If no solution exists, ``[]``.

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import quadratic_congruence
    >>> quadratic_congruence(2, 5, 3, 7) # 2x^2 + 5x + 3 = 0 (mod 7)
    [2, 6]
    >>> quadratic_congruence(8, 6, 4, 15) # No solution
    []

    See Also
    ========

    polynomial_congruence : Solve the polynomial congruence

    """
    a = as_int(a)
    b = as_int(b)
    c = as_int(c)
    n = as_int(n)
    if n <= 1:
        raise ValueError("n should be an integer greater than 1")
    a %= n
    b %= n
    c %= n

    if a == 0:
        return linear_congruence(b, -c, n)
    if n == 2:
        # assert a == 1
        roots = []
        if c == 0:
            roots.append(0)
        if (b + c) % 2:
            roots.append(1)
        return roots
    if gcd(2*a, n) == 1:
        inv_a = invert(a, n)
        b *= inv_a
        c *= inv_a
        if b % 2:
            b += n
        b >>= 1
        return sorted((i - b) % n for i in sqrt_mod_iter(b**2 - c, n))
    res = set()
    for i in sqrt_mod_iter(b**2 - 4*a*c, 4*a*n):
        q, rem = divmod(i - b, 2*a)
        if rem == 0:
            res.add(q % n)

    return sorted(res)

