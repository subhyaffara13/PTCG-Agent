
def test_basic_degree_2():
    d = 2
    knots = range(5)
    splines = bspline_basis_set(d, knots, x)
    b0 = Piecewise((x**2/2, Interval(0, 1).contains(x)),
                   (Rational(-3, 2) + 3*x - x**2, Interval(1, 2).contains(x)),
                   (Rational(9, 2) - 3*x + x**2/2, Interval(2, 3).contains(x)),
                   (0, True))
    b1 = Piecewise((S.Half - x + x**2/2, Interval(1, 2).contains(x)),
                   (Rational(-11, 2) + 5*x - x**2, Interval(2, 3).contains(x)),
                   (8 - 4*x + x**2/2, Interval(3, 4).contains(x)),
                   (0, True))
    assert splines[0] == b0
    assert splines[1] == b1

