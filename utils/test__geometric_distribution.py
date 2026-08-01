
def test_GeometricDistribution():
    p = S.One / 5
    d = GeometricDistribution(p)
    assert d.expectation(x, x) == 1/p
    assert d.expectation(x**2, x) - d.expectation(x, x)**2 == (1-p)/p**2
    assert abs(d.cdf(20000).evalf() - 1) < .001
    assert abs(d.cdf(20000.8).evalf() - 1) < .001
    G = Geometric('G', p=S(1)/4)
    assert cdf(G)(S(7)/2) == P(G <= S(7)/2)

    X = Geometric('X', Rational(1, 5))
    Y = Geometric('Y', Rational(3, 10))
    assert coskewness(X, X + Y, X + 2*Y).simplify() == sqrt(230)*Rational(81, 1150)

