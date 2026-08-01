
def test_issue_7001():
    from sympy.abc import r, R
    assert simplify(-(r*Piecewise((pi*Rational(4, 3), r <= R),
        (-8*pi*R**3/(3*r**3), True)) + 2*Piecewise((pi*r*Rational(4, 3), r <= R),
        (4*pi*R**3/(3*r**2), True)))/(4*pi*r)) == \
        Piecewise((-1, r <= R), (0, True))

