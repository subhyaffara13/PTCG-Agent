
def test_basic_degree_0():
    d = 0
    knots = range(5)
    splines = bspline_basis_set(d, knots, x)
    for i in range(len(splines)):
        assert splines[i] == Piecewise((1, Interval(i, i + 1).contains(x)),
                                       (0, True))

