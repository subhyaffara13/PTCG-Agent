
def laplace_correspondence(f, fdict, /):
    """
    This helper function takes a function `f` that is the result of a
    ``laplace_transform`` or an ``inverse_laplace_transform``.  It replaces all
    unevaluated ``LaplaceTransform(y(t), t, s)`` by `Y(s)` for any `s` and
    all ``InverseLaplaceTransform(Y(s), s, t)`` by `y(t)` for any `t` if
    ``fdict`` contains a correspondence ``{y: Y}``.

    Parameters
    ==========

    f : sympy expression
        Expression containing unevaluated ``LaplaceTransform`` or
        ``LaplaceTransform`` objects.
    fdict : dictionary
        Dictionary containing one or more function correspondences,
        e.g., ``{x: X, y: Y}`` meaning that ``X`` and ``Y`` are the
        Laplace transforms of ``x`` and ``y``, respectively.

    Examples
    ========

    >>> from sympy import laplace_transform, diff, Function
    >>> from sympy import laplace_correspondence, inverse_laplace_transform
    >>> from sympy.abc import t, s
    >>> y = Function("y")
    >>> Y = Function("Y")
    >>> z = Function("z")
    >>> Z = Function("Z")
    >>> f = laplace_transform(diff(y(t), t, 1) + z(t), t, s, noconds=True)
    >>> laplace_correspondence(f, {y: Y, z: Z})
    s*Y(s) + Z(s) - y(0)
    >>> f = inverse_laplace_transform(Y(s), s, t)
    >>> laplace_correspondence(f, {y: Y})
    y(t)
    """
    p = Wild('p')
    s = Wild('s')
    t = Wild('t')
    a = Wild('a')
    if (
            not isinstance(f, Expr)
            or (not f.has(LaplaceTransform)
                and not f.has(InverseLaplaceTransform))):
        return f
    for y, Y in fdict.items():
        if (
                (m := f.match(LaplaceTransform(y(a), t, s))) is not None
                and m[a] == m[t]):
            return Y(m[s])
        if (
                (m := f.match(InverseLaplaceTransform(Y(a), s, t, p)))
                is not None
                and m[a] == m[s]):
            return y(m[t])
    func = f.func
    args = [laplace_correspondence(arg, fdict) for arg in f.args]
    return func(*args)

