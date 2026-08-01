
def test_issue_8368i():
    from sympy.functions.elementary.complexes import arg, Abs
    assert integrate(exp(-s*x)*cosh(x), (x, 0, oo)) == \
        Piecewise(
            (   pi*Piecewise(
                    (   -s/(pi*(-s**2 + 1)),
                        Abs(s**2) < 1),
                    (   1/(pi*s*(1 - 1/s**2)),
                        Abs(s**(-2)) < 1),
                    (   meijerg(
                            ((S.Half,), (0, 0)),
                            ((0, S.Half), (0,)),
                            polar_lift(s)**2),
                        True)
                ),
                s**2 > 1
            ),
            (
                Integral(exp(-s*x)*cosh(x), (x, 0, oo)),
                True))
    assert integrate(exp(-s*x)*sinh(x), (x, 0, oo)) == \
        Piecewise(
            (   -1/(s + 1)/2 - 1/(-s + 1)/2,
                And(
                    Abs(s) > 1,
                    Abs(arg(s)) < pi/2,
                    Abs(arg(s)) <= pi/2
                    )),
            (   Integral(exp(-s*x)*sinh(x), (x, 0, oo)),
                True))

