
def test_basic_degree_1():
    d = 1
    knots = range(5)
    splines = bspline_basis_set(d, knots, x)
    assert splines[0] == Piecewise((x, Interval(0, 1).contains(x)),
                                   (2 - x, Interval(1, 2).contains(x)),
                                   (0, True))
    assert splines[1] == Piecewise((-1 + x, Interval(1, 2).contains(x)),
                                   (3 - x, Interval(2, 3).contains(x)),
                                   (0, True))
    assert splines[2] == Piecewise((-2 + x, Interval(2, 3).contains(x)),
                                   (4 - x, Interval(3, 4).contains(x)),
                                   (0, True))

