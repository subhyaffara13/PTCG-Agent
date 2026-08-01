
def test_gamma():
    k = Symbol("k", positive=True)
    theta = Symbol("theta", positive=True)

    X = Gamma('x', k, theta)

    # Tests characteristic function
    assert characteristic_function(X)(x) == ((-I*theta*x + 1)**(-k))

    assert density(X)(x) == x**(k - 1)*theta**(-k)*exp(-x/theta)/gamma(k)
    assert cdf(X, meijerg=True)(z) == Piecewise(
            (-k*lowergamma(k, 0)/gamma(k + 1) +
                k*lowergamma(k, z/theta)/gamma(k + 1), z >= 0),
            (0, True))

    # assert simplify(variance(X)) == k*theta**2  # handled numerically below
    assert E(X) == moment(X, 1)

    k, theta = symbols('k theta', positive=True)
    X = Gamma('x', k, theta)
    assert E(X) == k*theta
    assert variance(X) == k*theta**2
    assert skewness(X).expand() == 2/sqrt(k)
    assert kurtosis(X).expand() == 3 + 6/k

    Y = Gamma('y', 2*k, 3*theta)
    assert coskewness(X, theta*X + Y, k*X + Y).simplify() == \
        2*531441**(-k)*sqrt(k)*theta*(3*3**(12*k) - 2*531441**k) \
        /(sqrt(k**2 + 18)*sqrt(theta**2 + 18))


def test_gamma():
    assert Hyper_Function([2, 3], [-1]).gamma == 0
    assert Hyper_Function([-2, -3], [-1]).gamma == 2
    n = Dummy(integer=True)
    assert Hyper_Function([-1, n, 1], []).gamma == 1
    assert Hyper_Function([-1, -n, 1], []).gamma == 1
    p = Dummy(integer=True, positive=True)
    assert Hyper_Function([-1, p, 1], []).gamma == 1
    assert Hyper_Function([-1, -p, 1], []).gamma == 2


def test_gamma():
    a, b, x = symbols("a b x", positive=True)
    e = b**(-a)*x**(a - 1)*exp(-x/b)/gamma(a)
    Q = QQ[a, b].get_field()
    h1 = expr_to_holonomic(e, x, domain=Q)

    _, Dx = DifferentialOperators(Q.old_poly_ring(x), 'Dx')
    h2 = HolonomicFunction((-a + 1 + x/b) + (x)*Dx, x)

    assert h1 == h2


def test_gamma():
    assert gamma(nan) is nan
    assert gamma(oo) is oo

    assert gamma(-100) is zoo
    assert gamma(0) is zoo
    assert gamma(-100.0) is zoo

    assert gamma(1) == 1
    assert gamma(2) == 1
    assert gamma(3) == 2

    assert gamma(102) == factorial(101)

    assert gamma(S.Half) == sqrt(pi)

    assert gamma(Rational(3, 2)) == sqrt(pi)*S.Half
    assert gamma(Rational(5, 2)) == sqrt(pi)*Rational(3, 4)
    assert gamma(Rational(7, 2)) == sqrt(pi)*Rational(15, 8)

    assert gamma(Rational(-1, 2)) == -2*sqrt(pi)
    assert gamma(Rational(-3, 2)) == sqrt(pi)*Rational(4, 3)
    assert gamma(Rational(-5, 2)) == sqrt(pi)*Rational(-8, 15)

    assert gamma(Rational(-15, 2)) == sqrt(pi)*Rational(256, 2027025)

    assert gamma(Rational(
        -11, 8)).expand(func=True) == Rational(64, 33)*gamma(Rational(5, 8))
    assert gamma(Rational(
        -10, 3)).expand(func=True) == Rational(81, 280)*gamma(Rational(2, 3))
    assert gamma(Rational(
        14, 3)).expand(func=True) == Rational(880, 81)*gamma(Rational(2, 3))
    assert gamma(Rational(
        17, 7)).expand(func=True) == Rational(30, 49)*gamma(Rational(3, 7))
    assert gamma(Rational(
        19, 8)).expand(func=True) == Rational(33, 64)*gamma(Rational(3, 8))

    assert gamma(x).diff(x) == gamma(x)*polygamma(0, x)

    assert gamma(x - 1).expand(func=True) == gamma(x)/(x - 1)
    assert gamma(x + 2).expand(func=True, mul=False) == x*(x + 1)*gamma(x)

    assert conjugate(gamma(x)) == gamma(conjugate(x))

    assert expand_func(gamma(x + Rational(3, 2))) == \
        (x + S.Half)*gamma(x + S.Half)

    assert expand_func(gamma(x - S.Half)) == \
        gamma(S.Half + x)/(x - S.Half)

    # Test a bug:
    assert expand_func(gamma(x + Rational(3, 4))) == gamma(x + Rational(3, 4))

    # XXX: Not sure about these tests. I can fix them by defining e.g.
    # exp_polar.is_integer but I'm not sure if that makes sense.
    assert gamma(3*exp_polar(I*pi)/4).is_nonnegative is False
    assert gamma(3*exp_polar(I*pi)/4).is_extended_nonpositive is True

    y = Symbol('y', nonpositive=True, integer=True)
    assert gamma(y).is_real == False
    y = Symbol('y', positive=True, noninteger=True)
    assert gamma(y).is_real == True

    assert gamma(-1.0, evaluate=False).is_real == False
    assert gamma(0, evaluate=False).is_real == False
    assert gamma(-2, evaluate=False).is_real == False


def test_gamma():
    mp.dps = 15
    assert gamma(0.25).ae(3.6256099082219083119)
    assert gamma(0.0001).ae(9999.4228832316241908)
    assert gamma(300).ae('1.0201917073881354535e612')
    assert gamma(-0.5).ae(-3.5449077018110320546)
    assert gamma(-7.43).ae(0.00026524416464197007186)
    #assert gamma(Rational(1,2)) == gamma(0.5)
    #assert gamma(Rational(-7,3)).ae(gamma(mpf(-7)/3))
    assert gamma(1+1j).ae(0.49801566811835604271 - 0.15494982830181068512j)
    assert gamma(-1+0.01j).ae(-0.422733904013474115 + 99.985883082635367436j)
    assert gamma(20+30j).ae(-1453876687.5534810 + 1163777777.8031573j)
    # Should always give exact factorials when they can
    # be represented as mpfs under the current working precision
    fact = 1
    for i in range(1, 18):
        assert gamma(i) == fact
        fact *= i
    for dps in [170, 600]:
        fact = 1
        mp.dps = dps
        for i in range(1, 105):
            assert gamma(i) == fact
            fact *= i
    mp.dps = 100
    assert gamma(0.5).ae(sqrt(pi))
    mp.dps = 15
    assert factorial(0) == fac(0) == 1
    assert factorial(3) == 6
    assert isnan(gamma(nan))
    assert gamma(1100).ae('4.8579168073569433667e2866')
    assert rgamma(0) == 0
    assert rgamma(-1) == 0
    assert rgamma(2) == 1.0
    assert rgamma(3) == 0.5
    assert loggamma(2+8j).ae(-8.5205176753667636926 + 10.8569497125597429366j)
    assert loggamma('1e10000').ae('2.302485092994045684017991e10004')
    assert loggamma('1e10000j').ae(mpc('-1.570796326794896619231322e10000','2.302485092994045684017991e10004'))

