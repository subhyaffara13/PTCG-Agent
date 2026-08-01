
def test_JointRV():
    x1, x2 = (Indexed('x', i) for i in (1, 2))
    pdf = exp(-x1**2/2 + x1 - x2**2/2 - S.Half)/(2*pi)
    X = JointRV('x', pdf)
    assert density(X)(1, 2) == exp(-2)/(2*pi)
    assert isinstance(X.pspace.distribution, JointDistributionHandmade)
    assert marginal_distribution(X, 0)(2) == sqrt(2)*exp(Rational(-1, 2))/(2*sqrt(pi))

