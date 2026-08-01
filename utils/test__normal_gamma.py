
def test_NormalGamma():
    ng = NormalGamma('G', 1, 2, 3, 4)
    assert density(ng)(1, 1) == 32*exp(-4)/sqrt(pi)
    assert ng.pspace.distribution.set == ProductSet(S.Reals, Interval(0, oo))
    raises(ValueError, lambda:NormalGamma('G', 1, 2, 3, -1))
    assert marginal_distribution(ng, 0)(1) == \
        3*sqrt(10)*gamma(Rational(7, 4))/(10*sqrt(pi)*gamma(Rational(5, 4)))
    assert marginal_distribution(ng, y)(1) == exp(Rational(-1, 4))/128
    assert marginal_distribution(ng,[0,1])(x) == x**2*exp(-x/4)/128

