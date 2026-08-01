
def test_multiple_normal():
    X, Y = Normal('x', 0, 1), Normal('y', 0, 1)
    p = Symbol("p", positive=True)

    assert E(X + Y) == 0
    assert variance(X + Y) == 2
    assert variance(X + X) == 4
    assert covariance(X, Y) == 0
    assert covariance(2*X + Y, -X) == -2*variance(X)
    assert skewness(X) == 0
    assert skewness(X + Y) == 0
    assert kurtosis(X) == 3
    assert kurtosis(X+Y) == 3
    assert correlation(X, Y) == 0
    assert correlation(X, X + Y) == correlation(X, X - Y)
    assert moment(X, 2) == 1
    assert cmoment(X, 3) == 0
    assert moment(X + Y, 4) == 12
    assert cmoment(X, 2) == variance(X)
    assert smoment(X*X, 2) == 1
    assert smoment(X + Y, 3) == skewness(X + Y)
    assert smoment(X + Y, 4) == kurtosis(X + Y)
    assert E(X, Eq(X + Y, 0)) == 0
    assert variance(X, Eq(X + Y, 0)) == S.Half
    assert quantile(X)(p) == sqrt(2)*erfinv(2*p - S.One)

