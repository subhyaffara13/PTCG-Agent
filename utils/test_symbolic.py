
def test_symbolic():
    mu1, mu2 = symbols('mu1 mu2', real=True)
    s1, s2 = symbols('sigma1 sigma2', positive=True)
    rate = Symbol('lambda', positive=True)
    X = Normal('x', mu1, s1)
    Y = Normal('y', mu2, s2)
    Z = Exponential('z', rate)
    a, b, c = symbols('a b c', real=True)

    assert E(X) == mu1
    assert E(X + Y) == mu1 + mu2
    assert E(a*X + b) == a*E(X) + b
    assert variance(X) == s1**2
    assert variance(X + a*Y + b) == variance(X) + a**2*variance(Y)

    assert E(Z) == 1/rate
    assert E(a*Z + b) == a*E(Z) + b
    assert E(X + a*Z + b) == mu1 + a/rate + b
    assert median(X) == FiniteSet(mu1)

