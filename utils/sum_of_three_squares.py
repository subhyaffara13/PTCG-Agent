
def sum_of_three_squares(n):
    r"""
    Returns a 3-tuple $(a, b, c)$ such that $a^2 + b^2 + c^2 = n$ and
    $a, b, c \geq 0$.

    Returns None if $n = 4^a(8m + 7)$ for some `a, m \in \mathbb{Z}`. See
    [1]_ for more details.

    Parameters
    ==========

    n : Integer
        non-negative integer

    Returns
    =======

    (int, int, int) | None : 3-tuple non-negative integers ``(a, b, c)`` satisfying ``a**2 + b**2 + c**2 = n``.
                             a,b,c are sorted in ascending order. ``None`` if no such ``(a,b,c)``.

    Raises
    ======

    ValueError
        If ``n`` is a negative integer

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import sum_of_three_squares
    >>> sum_of_three_squares(44542)
    (18, 37, 207)

    References
    ==========

    .. [1] Representing a number as a sum of three squares, [online],
        Available: https://schorn.ch/lagrange.html

    See Also
    ========

    power_representation :
        ``sum_of_three_squares(n)`` is one of the solutions output by ``power_representation(n, 2, 3, zeros=True)``

    """
    # https://math.stackexchange.com/questions/483101/rabin-and-shallit-algorithm/651425#651425
    # discusses these numbers (except for 1, 2, 3) as the exceptions of H&L's conjecture that
    # Every sufficiently large number n is either a square or the sum of a prime and a square.
    special = {1: (0, 0, 1), 2: (0, 1, 1), 3: (1, 1, 1), 10: (0, 1, 3), 34: (3, 3, 4),
               58: (0, 3, 7), 85: (0, 6, 7), 130: (0, 3, 11), 214: (3, 6, 13), 226: (8, 9, 9),
               370: (8, 9, 15), 526: (6, 7, 21), 706: (15, 15, 16), 730: (0, 1, 27),
               1414: (6, 17, 33), 1906: (13, 21, 36), 2986: (21, 32, 39), 9634: (56, 57, 57)}
    n = as_int(n)
    if n < 0:
        raise ValueError("n should be a non-negative integer")
    if n == 0:
        return (0, 0, 0)
    n, v = remove(n, 4)
    v = 1 << v
    if n % 8 == 7:
        return
    if n in special:
        return tuple([v*i for i in special[n]])

    s, _exact = integer_nthroot(n, 2)
    if _exact:
        return (0, 0, v*s)
    if n % 8 == 3:
        if not s % 2:
            s -= 1
        for x in range(s, -1, -2):
            N = (n - x**2) // 2
            if isprime(N):
                # n % 8 == 3 and x % 2 == 1 => N % 4 == 1
                y, z = prime_as_sum_of_two_squares(N)
                return tuple(sorted([v*x, v*(y + z), v*abs(y - z)]))
        # We will never reach this point because there must be a solution.
        assert False

    # assert n % 4 in [1, 2]
    if not((n % 2) ^ (s % 2)):
        s -= 1
    for x in range(s, -1, -2):
        N = n - x**2
        if isprime(N):
            # assert N % 4 == 1
            y, z = prime_as_sum_of_two_squares(N)
            return tuple(sorted([v*x, v*y, v*z]))
    # We will never reach this point because there must be a solution.
    assert False

