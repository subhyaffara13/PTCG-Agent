
def test_ContinuousRV():
    pdf = sqrt(2)*exp(-x**2/2)/(2*sqrt(pi))  # Normal distribution
    # X and Y should be equivalent
    X = ContinuousRV(x, pdf, check=True)
    Y = Normal('y', 0, 1)

    assert variance(X) == variance(Y)
    assert P(X > 0) == P(Y > 0)
    Z = ContinuousRV(z, exp(-z), set=Interval(0, oo))
    assert Z.pspace.domain.set == Interval(0, oo)
    assert E(Z) == 1
    assert P(Z > 5) == exp(-5)
    raises(ValueError, lambda: ContinuousRV(z, exp(-z), set=Interval(0, 10), check=True))

    # the correct pdf for Gamma(k, theta) but the integral in `check`
    # integrates to something equivalent to 1 and not to 1 exactly
    _x, k, theta = symbols("x k theta", positive=True)
    pdf = 1/(gamma(k)*theta**k)*_x**(k-1)*exp(-_x/theta)
    X = ContinuousRV(_x, pdf, set=Interval(0, oo))
    Y = Gamma('y', k, theta)
    assert (E(X) - E(Y)).simplify() == 0
    assert (variance(X) - variance(Y)).simplify() == 0

