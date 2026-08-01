
def test_repeated_degree_2():
    d = 2
    knots = [0, 0, 1, 2, 2, 3, 4, 4]
    splines = bspline_basis_set(d, knots, x)

    assert splines[0] == Piecewise(((-3*x**2/2 + 2*x), And(x <= 1, x >= 0)),
                                   (x**2/2 - 2*x + 2, And(x <= 2, x >= 1)),
                                   (0, True))
    assert splines[1] == Piecewise((x**2/2, And(x <= 1, x >= 0)),
                                   (-3*x**2/2 + 4*x - 2, And(x <= 2, x >= 1)),
                                   (0, True))
    assert splines[2] == Piecewise((x**2 - 2*x + 1, And(x <= 2, x >= 1)),
                                   (x**2 - 6*x + 9, And(x <= 3, x >= 2)),
                                   (0, True))
    assert splines[3] == Piecewise((-3*x**2/2 + 8*x - 10, And(x <= 3, x >= 2)),
                                   (x**2/2 - 4*x + 8, And(x <= 4, x >= 3)),
                                   (0, True))
    assert splines[4] == Piecewise((x**2/2 - 2*x + 2, And(x <= 3, x >= 2)),
                                   (-3*x**2/2 + 10*x - 16, And(x <= 4, x >= 3)),
                                   (0, True))

