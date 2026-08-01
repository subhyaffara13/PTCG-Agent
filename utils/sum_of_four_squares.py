
def sum_of_four_squares(n):
    r"""
    Returns a 4-tuple `(a, b, c, d)` such that `a^2 + b^2 + c^2 + d^2 = n`.
    Here `a, b, c, d \geq 0`.

    Parameters
    ==========

    n : Integer
        non-negative integer

    Returns
    =======

    (int, int, int, int) : 4-tuple non-negative integers ``(a, b, c, d)`` satisfying ``a**2 + b**2 + c**2 + d**2 = n``.
                           a,b,c,d are sorted in ascending order.

    Raises
    ======

    ValueError
        If ``n`` is a negative integer

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import sum_of_four_squares
    >>> sum_of_four_squares(3456)
    (8, 8, 32, 48)
    >>> sum_of_four_squares(1294585930293)
    (0, 1234, 2161, 1137796)

    References
    ==========

    .. [1] Representing a number as a sum of four squares, [online],
        Available: https://schorn.ch/lagrange.html

    See Also
    ========

    power_representation :
        ``sum_of_four_squares(n)`` is one of the solutions output by ``power_representation(n, 2, 4, zeros=True)``

    """
    n = as_int(n)
    if n < 0:
        raise ValueError("n should be a non-negative integer")
    if n == 0:
        return (0, 0, 0, 0)
    # remove factors of 4 since a solution in terms of 3 squares is
    # going to be returned; this is also done in sum_of_three_squares,
    # but it needs to be done here to select d
    n, v = remove(n, 4)
    v = 1 << v
    if n % 8 == 7:
        d = 2
        n = n - 4
    elif n % 8 in (2, 6):
        d = 1
        n = n - 1
    else:
        d = 0
    x, y, z = sum_of_three_squares(n)  # sorted
    return tuple(sorted([v*d, v*x, v*y, v*z]))

