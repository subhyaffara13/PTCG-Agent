
def test_bernoulli():
    p, a, b, t = symbols('p a b t')
    X = Bernoulli('B', p, a, b)

    assert E(X) == a*p + b*(-p + 1)
    assert density(X)[a] == p
    assert density(X)[b] == 1 - p
    assert characteristic_function(X)(t) == p * exp(I * a * t) + (-p + 1) * exp(I * b * t)
    assert moment_generating_function(X)(t) == p * exp(a * t) + (-p + 1) * exp(b * t)

    X = Bernoulli('B', p, 1, 0)
    z = Symbol("z")

    assert E(X) == p
    assert simplify(variance(X)) == p*(1 - p)
    assert E(a*X + b) == a*E(X) + b
    assert simplify(variance(a*X + b)) == simplify(a**2 * variance(X))
    assert quantile(X)(z) == Piecewise((nan, (z > 1) | (z < 0)), (0, z <= 1 - p), (1, z <= 1))
    Y = Bernoulli('Y', Rational(1, 2))
    assert median(Y) == FiniteSet(0, 1)
    Z = Bernoulli('Z', Rational(2, 3))
    assert median(Z) == FiniteSet(1)
    raises(ValueError, lambda: Bernoulli('B', 1.5))
    raises(ValueError, lambda: Bernoulli('B', -0.5))

    #issue 8248
    assert X.pspace.compute_expectation(1) == 1

    p = Rational(1, 5)
    X = Binomial('X', 5, p)
    Y = Binomial('Y', 7, 2*p)
    Z = Binomial('Z', 9, 3*p)
    assert coskewness(Y + Z, X + Y, X + Z).simplify() == 0
    assert coskewness(Y + 2*X + Z, X + 2*Y + Z, X + 2*Z + Y).simplify() == \
                        sqrt(1529)*Rational(12, 16819)
    assert coskewness(Y + 2*X + Z, X + 2*Y + Z, X + 2*Z + Y, X < 2).simplify() \
                        == -sqrt(357451121)*Rational(2812, 4646864573)


def test_bernoulli():
    assert bernoulli(0) == 1
    assert bernoulli(1) == Rational(1, 2)
    assert bernoulli(2) == Rational(1, 6)
    assert bernoulli(3) == 0
    assert bernoulli(4) == Rational(-1, 30)
    assert bernoulli(5) == 0
    assert bernoulli(6) == Rational(1, 42)
    assert bernoulli(7) == 0
    assert bernoulli(8) == Rational(-1, 30)
    assert bernoulli(10) == Rational(5, 66)
    assert bernoulli(1000001) == 0

    assert bernoulli(0, x) == 1
    assert bernoulli(1, x) == x - S.Half
    assert bernoulli(2, x) == x**2 - x + Rational(1, 6)
    assert bernoulli(3, x) == x**3 - (3*x**2)/2 + x/2

    # Should be fast; computed with mpmath
    b = bernoulli(1000)
    assert b.p % 10**10 == 7950421099
    assert b.q == 342999030

    b = bernoulli(10**6, evaluate=False).evalf()
    assert str(b) == '-2.23799235765713e+4767529'

    # Issue #8527
    l = Symbol('l', integer=True)
    m = Symbol('m', integer=True, nonnegative=True)
    n = Symbol('n', integer=True, positive=True)
    assert isinstance(bernoulli(2 * l + 1), bernoulli)
    assert isinstance(bernoulli(2 * m + 1), bernoulli)
    assert bernoulli(2 * n + 1) == 0

    assert bernoulli(x, 1) == bernoulli(x)

    assert str(bernoulli(0.0, 2.3).evalf(n=10)) == '1.000000000'
    assert str(bernoulli(1.0).evalf(n=10)) == '0.5000000000'
    assert str(bernoulli(1.2).evalf(n=10)) == '0.4195995367'
    assert str(bernoulli(1.2, 0.8).evalf(n=10)) == '0.2144830348'
    assert str(bernoulli(1.2, -0.8).evalf(n=10)) == '-1.158865646 - 0.6745558744*I'
    assert str(bernoulli(3.0, 1j).evalf(n=10)) == '1.5 - 0.5*I'
    assert str(bernoulli(I).evalf(n=10)) == '0.9268485643 - 0.5821580598*I'
    assert str(bernoulli(I, I).evalf(n=10)) == '0.1267792071 + 0.01947413152*I'
    assert bernoulli(x).evalf() == bernoulli(x)


def test_bernoulli():
    assert bernfrac(0) == (1,1)
    assert bernfrac(1) == (-1,2)
    assert bernfrac(2) == (1,6)
    assert bernfrac(3) == (0,1)
    assert bernfrac(4) == (-1,30)
    assert bernfrac(5) == (0,1)
    assert bernfrac(6) == (1,42)
    assert bernfrac(8) == (-1,30)
    assert bernfrac(10) == (5,66)
    assert bernfrac(12) == (-691,2730)
    assert bernfrac(18) == (43867,798)
    p, q = bernfrac(228)
    assert p % 10**10 == 164918161
    assert q == 625170
    p, q = bernfrac(1000)
    assert p % 10**10 == 7950421099
    assert q == 342999030
    mp.dps = 15
    assert bernoulli(0) == 1
    assert bernoulli(1) == -0.5
    assert bernoulli(2).ae(1./6)
    assert bernoulli(3) == 0
    assert bernoulli(4).ae(-1./30)
    assert bernoulli(5) == 0
    assert bernoulli(6).ae(1./42)
    assert str(bernoulli(10)) == '0.0757575757575758'
    assert str(bernoulli(234)) == '7.62772793964344e+267'
    assert str(bernoulli(10**5)) == '-5.82229431461335e+376755'
    assert str(bernoulli(10**8+2)) == '1.19570355039953e+676752584'

    mp.dps = 50
    assert str(bernoulli(10)) == '0.075757575757575757575757575757575757575757575757576'
    assert str(bernoulli(234)) == '7.6277279396434392486994969020496121553385863373331e+267'
    assert str(bernoulli(10**5)) == '-5.8222943146133508236497045360612887555320691004308e+376755'
    assert str(bernoulli(10**8+2)) == '1.1957035503995297272263047884604346914602088317782e+676752584'

    mp.dps = 1000
    assert bernoulli(10).ae(mpf(5)/66)

    mp.dps = 50000
    assert bernoulli(10).ae(mpf(5)/66)

    mp.dps = 15

