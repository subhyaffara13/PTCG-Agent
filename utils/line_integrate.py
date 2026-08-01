
def line_integrate(field, curve, vars):
    """line_integrate(field, Curve, variables)

    Compute the line integral.

    Examples
    ========

    >>> from sympy import Curve, line_integrate, E, ln
    >>> from sympy.abc import x, y, t
    >>> C = Curve([E**t + 1, E**t - 1], (t, 0, ln(2)))
    >>> line_integrate(x + y, C, [x, y])
    3*sqrt(2)

    See Also
    ========

    sympy.integrals.integrals.integrate, Integral
    """
    from sympy.geometry import Curve
    F = sympify(field)
    if not F:
        raise ValueError(
            "Expecting function specifying field as first argument.")
    if not isinstance(curve, Curve):
        raise ValueError("Expecting Curve entity as second argument.")
    if not is_sequence(vars):
        raise ValueError("Expecting ordered iterable for variables.")
    if len(curve.functions) != len(vars):
        raise ValueError("Field variable size does not match curve dimension.")

    if curve.parameter in vars:
        raise ValueError("Curve parameter clashes with field parameters.")

    # Calculate derivatives for line parameter functions
    # F(r) -> F(r(t)) and finally F(r(t)*r'(t))
    Ft = F
    dldt = 0
    for i, var in enumerate(vars):
        _f = curve.functions[i]
        _dn = diff(_f, curve.parameter)
        # ...arc length
        dldt = dldt + (_dn * _dn)
        Ft = Ft.subs(var, _f)
    Ft = Ft * sqrt(dldt)

    integral = Integral(Ft, curve.limits).doit(deep=False)
    return integral

