
def test_containment():
    a, b, c, d, e = [1, 2, 3, 4, 5]
    p = (Piecewise((d, x > 1), (e, True))*
        Piecewise((a, Abs(x - 1) < 1), (b, Abs(x - 2) < 2), (c, True)))
    assert p.integrate(x).diff(x) == Piecewise(
        (c*e, x <= 0),
        (a*e, x <= 1),
        (a*d, x < 2),  # this is what we want to get right
        (b*d, x < 4),
        (c*d, True))

