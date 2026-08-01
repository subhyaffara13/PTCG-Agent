
def test_rs_swap():
    X = Normal('x', 0, 1)
    Y = Exponential('y', 1)

    XX = Normal('x', 0, 2)
    YY = Normal('y', 0, 3)

    expr = 2*X + Y
    assert expr.subs(rs_swap((X, Y), (YY, XX))) == 2*XX + YY

