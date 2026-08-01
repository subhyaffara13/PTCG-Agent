
def is_infinite(expr) -> bool:
    """Check if an expression is any type of infinity (positive or negative).

    This handles both sympy's built-in infinities (oo, -oo) and PyTorch's
    integer infinities (int_oo, -int_oo).

    Note: We cannot rely on sympy's is_finite property because IntInfinity
    and NegativeIntInfinity have is_integer=True, which implies is_finite=True
    in sympy's assumption system.
    """
    return expr in (
        S.Infinity,
        S.NegativeInfinity,
        S.IntInfinity,
        S.NegativeIntInfinity,
    )


def is_infinite(obj, assumptions=None):
    if assumptions is None:
        return obj.is_infinite
    return ask(Q.infinite(obj), assumptions)

