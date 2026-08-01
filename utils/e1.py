
def e1(z):
    # hack to get consistent signs if the imaginary part if 0
    # and signed
    typez = type(z)
    if type(z) not in (float, complex):
        try:
            z = float(z)
            typez = float
        except (TypeError, ValueError):
            z = complex(z)
            typez = complex
    if typez is complex and not z.imag:
        z = complex(z.real, 0.0)
    # end hack
    return -ei(-z, _e1=True)


def E1(z):
    """
    Classical case of the generalized exponential integral.

    Explanation
    ===========

    This is equivalent to ``expint(1, z)``.

    Examples
    ========

    >>> from sympy import E1
    >>> E1(0)
    expint(1, 0)

    >>> E1(5)
    expint(1, 5)

    See Also
    ========

    Ei: Exponential integral.
    expint: Generalised exponential integral.
    li: Logarithmic integral.
    Li: Offset logarithmic integral.
    Si: Sine integral.
    Ci: Cosine integral.
    Shi: Hyperbolic sine integral.
    Chi: Hyperbolic cosine integral.

    """
    return expint(1, z)


def e1(ctx, z):
    try:
        return ctx._e1(z)
    except NotImplementedError:
        return ctx.expint(1, z)

