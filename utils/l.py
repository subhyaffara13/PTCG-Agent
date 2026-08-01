
def L(rv):
    """Return count of trigonometric functions in expression.

    Examples
    ========

    >>> from sympy.simplify.fu import L
    >>> from sympy.abc import x
    >>> from sympy import cos, sin
    >>> L(cos(x)+sin(x))
    2
    """
    return S(rv.count(TrigonometricFunction))


def L(A):
    yield aslinearoperator(A)

