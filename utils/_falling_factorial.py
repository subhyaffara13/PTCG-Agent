
def _falling_factorial(x, n):
    r"""
    Return the factorial of `x` to the `n` falling.

    This is defined as:

    .. math::   x^\underline n = (x)_n = x (x-1) \cdots (x-n+1)

    This can more efficiently calculate ratios of factorials, since:

    n!/m! == falling_factorial(n, n-m)

    where n >= m

    skipping the factors that cancel out

    the usual factorial n! == ff(n, n)
    """
    val = 1
    for k in range(x - n + 1, x + 1):
        val *= k
    return val

