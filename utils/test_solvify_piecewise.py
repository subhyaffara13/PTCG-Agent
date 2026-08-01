
def test_solvify_piecewise():
    p1 = Piecewise((0, x < -1), (x**2, x <= 1), (log(x), True))
    p2 = Piecewise((0, x < -10), (x**2 + 5*x - 6, x >= -9))
    p3 = Piecewise((0, Eq(x, 0)), (x**2/Abs(x), True))
    p4 = Piecewise((0, Eq(x, pi)), ((x - pi)/sin(x), True))

    # issue 21079
    assert solvify(p1, x, S.Reals) == [0]
    assert solvify(p2, x, S.Reals) == [-6, 1]
    assert solvify(p3, x, S.Reals) == [0]
    assert solvify(p4, x, S.Reals) == [pi]

