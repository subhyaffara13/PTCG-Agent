
def covariance(X, Y, condition=None, **kwargs):
    """
    Covariance of two random expressions.

    Explanation
    ===========

    The expectation that the two variables will rise and fall together

    .. math::
        covariance(X,Y) = E((X-E(X)) (Y-E(Y)))

    Examples
    ========

    >>> from sympy.stats import Exponential, covariance
    >>> from sympy import Symbol

    >>> rate = Symbol('lambda', positive=True, real=True)
    >>> X = Exponential('X', rate)
    >>> Y = Exponential('Y', rate)

    >>> covariance(X, X)
    lambda**(-2)
    >>> covariance(X, Y)
    0
    >>> covariance(X, Y + rate*X)
    1/lambda
    """
    if (is_random(X) and pspace(X) == PSpace()) or (is_random(Y) and pspace(Y) == PSpace()):
        from sympy.stats.symbolic_probability import Covariance
        return Covariance(X, Y, condition)

    return expectation(
        (X - expectation(X, condition, **kwargs)) *
        (Y - expectation(Y, condition, **kwargs)),
        condition, **kwargs)

