
def test_match_terms():
    X, Y = map(Wild, "XY")
    x, y, z = symbols('x y z')
    assert (5*y - x).match(5*X - Y) == {X: y, Y: x}
    # 15907
    assert (x + (y - 1)*z).match(x + X*z) == {X: y - 1}
    # 20747
    assert (x - log(x/y)*(1-exp(x/y))).match(x - log(X/y)*(1-exp(x/y))) == {X: x}

