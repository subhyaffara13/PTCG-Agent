
def test_normal_CompoundDist():
    X = Normal('X', 1, 2)
    Y = Normal('X', X, 4)
    assert density(Y)(x).simplify() == sqrt(10)*exp(-x**2/40 + x/20 - S(1)/40)/(20*sqrt(pi))
    assert E(Y) == 1 # it is always equal to mean of X
    assert P(Y > 1) == S(1)/2 # as 1 is the mean
    assert P(Y > 5).simplify() ==  S(1)/2 - erf(sqrt(10)/5)/2
    assert variance(Y) == variance(X) + 4**2 # 2**2 + 4**2

