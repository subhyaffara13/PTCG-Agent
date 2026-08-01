
def prime_as_sum_of_two_squares(p):
    """
    Represent a prime `p` as a unique sum of two squares; this can
    only be done if the prime is congruent to 1 mod 4.

    Parameters
    ==========

    p : Integer
        A prime that is congruent to 1 mod 4

    Returns
    =======

    (int, int) | None : Pair of positive integers ``(x, y)`` satisfying ``x**2 + y**2 = p``.
                        None if ``p`` is not congruent to 1 mod 4.

    Raises
    ======

    ValueError
        If ``p`` is not prime number

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import prime_as_sum_of_two_squares
    >>> prime_as_sum_of_two_squares(7)  # can't be done
    >>> prime_as_sum_of_two_squares(5)
    (1, 2)

    Reference
    =========

    .. [1] Representing a number as a sum of four squares, [online],
           Available: https://schorn.ch/lagrange.html

    See Also
    ========

    sum_of_squares

    """
    p = as_int(p)
    if p % 4 != 1:
        return
    if not isprime(p):
        raise ValueError("p should be a prime number")

    if p % 8 == 5:
        # Legendre symbol (2/p) == -1 if p % 8 in [3, 5]
        b = 2
    elif p % 12 == 5:
        # Legendre symbol (3/p) == -1 if p % 12 in [5, 7]
        b = 3
    elif p % 5 in [2, 3]:
        # Legendre symbol (5/p) == -1 if p % 5 in [2, 3]
        b = 5
    else:
        b = 7
        while jacobi(b, p) == 1:
            b = nextprime(b)

    b = pow(b, p >> 2, p)
    a = p
    while b**2 > p:
        a, b = b, a % b
    return (int(a % b), int(b))  # convert from long

