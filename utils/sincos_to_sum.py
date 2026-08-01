
def sincos_to_sum(expr):
    """Convert products and powers of sin and cos to sums.

    Explanation
    ===========

    Applied power reduction TRpower first, then expands products, and
    converts products to sums with TR8.

    Examples
    ========

    >>> from sympy.simplify.fu import sincos_to_sum
    >>> from sympy.abc import x
    >>> from sympy import cos, sin
    >>> sincos_to_sum(16*sin(x)**3*cos(2*x)**2)
    7*sin(x) - 5*sin(3*x) + 3*sin(5*x) - sin(7*x)
    """

    if not expr.has(cos, sin):
        return expr
    else:
        return TR8(expand_mul(TRpower(expr)))

