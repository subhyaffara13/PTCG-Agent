
def test_NormalDistribution():
    nd = NormalDistribution(0, 1)
    x = Symbol('x')
    assert nd.cdf(x) == erf(sqrt(2)*x/2)/2 + S.Half
    assert nd.expectation(1, x) == 1
    assert nd.expectation(x, x) == 0
    assert nd.expectation(x**2, x) == 1
    #Test issue 10076
    a = SingleContinuousPSpace(x, NormalDistribution(2, 4))
    _z = Dummy('_z')

    expected1 = Integral(sqrt(2)*exp(-(_z - 2)**2/32)/(8*sqrt(pi)),(_z, -oo, 1))
    assert a.probability(x < 1, evaluate=False).dummy_eq(expected1) is True

    expected2 = Integral(sqrt(2)*exp(-(_z - 2)**2/32)/(8*sqrt(pi)),(_z, 1, oo))
    assert a.probability(x > 1, evaluate=False).dummy_eq(expected2) is True

    b = SingleContinuousPSpace(x, NormalDistribution(1, 9))

    expected3 = Integral(sqrt(2)*exp(-(_z - 1)**2/162)/(18*sqrt(pi)),(_z, 6, oo))
    assert b.probability(x > 6, evaluate=False).dummy_eq(expected3) is True

    expected4 = Integral(sqrt(2)*exp(-(_z - 1)**2/162)/(18*sqrt(pi)),(_z, -oo, 6))
    assert b.probability(x < 6, evaluate=False).dummy_eq(expected4) is True

