
def test_gegenbauer():
    n = Symbol("n")
    a = Symbol("a")

    assert gegenbauer(0, a, x) == 1
    assert gegenbauer(1, a, x) == 2*a*x
    assert gegenbauer(2, a, x) == -a + x**2*(2*a**2 + 2*a)
    assert gegenbauer(3, a, x) == \
        x**3*(4*a**3/3 + 4*a**2 + a*Rational(8, 3)) + x*(-2*a**2 - 2*a)

    assert gegenbauer(-1, a, x) == 0
    assert gegenbauer(n, S.Half, x) == legendre(n, x)
    assert gegenbauer(n, 1, x) == chebyshevu(n, x)
    assert gegenbauer(n, -1, x) == 0

    X = gegenbauer(n, a, x)
    assert isinstance(X, gegenbauer)

    assert gegenbauer(n, a, -x) == (-1)**n*gegenbauer(n, a, x)
    assert gegenbauer(n, a, 0) == 2**n*sqrt(pi) * \
        gamma(a + n/2)/(gamma(a)*gamma(-n/2 + S.Half)*gamma(n + 1))
    assert gegenbauer(n, a, 1) == gamma(2*a + n)/(gamma(2*a)*gamma(n + 1))

    assert gegenbauer(n, Rational(3, 4), -1) is zoo
    assert gegenbauer(n, Rational(1, 4), -1) == (sqrt(2)*cos(pi*(n + S.One/4))*
                      gamma(n + S.Half)/(sqrt(pi)*gamma(n + 1)))

    m = Symbol("m", positive=True)
    assert gegenbauer(m, a, oo) == oo*RisingFactorial(a, m)
    assert unchanged(gegenbauer, n, a, oo)

    assert conjugate(gegenbauer(n, a, x)) == gegenbauer(n, conjugate(a), conjugate(x))

    _k = Dummy('k')

    assert diff(gegenbauer(n, a, x), n) == Derivative(gegenbauer(n, a, x), n)
    assert diff(gegenbauer(n, a, x), a).dummy_eq(Sum((2*(-1)**(-_k + n) + 2)*
        (_k + a)*gegenbauer(_k, a, x)/((-_k + n)*(_k + 2*a + n)) + ((2*_k +
        2)/((_k + 2*a)*(2*_k + 2*a + 1)) + 2/(_k + 2*a + n))*gegenbauer(n, a
        , x), (_k, 0, n - 1)))
    assert diff(gegenbauer(n, a, x), x) == 2*a*gegenbauer(n - 1, a + 1, x)

    assert gegenbauer(n, a, x).rewrite(Sum).dummy_eq(
        Sum((-1)**_k*(2*x)**(-2*_k + n)*RisingFactorial(a, -_k + n)
        /(factorial(_k)*factorial(-2*_k + n)), (_k, 0, floor(n/2))))
    assert gegenbauer(n, a, x).rewrite("polynomial").dummy_eq(
        Sum((-1)**_k*(2*x)**(-2*_k + n)*RisingFactorial(a, -_k + n)
        /(factorial(_k)*factorial(-2*_k + n)), (_k, 0, floor(n/2))))

    raises(ArgumentIndexError, lambda: gegenbauer(n, a, x).fdiff(4))


def test_gegenbauer():
    mp.dps = 15
    assert gegenbauer(1,2,3).ae(12)
    assert gegenbauer(2,3,4).ae(381)
    assert gegenbauer(0,0,0) == 0
    assert gegenbauer(2,-1,3) == 0
    assert gegenbauer(-7, 0.5, 3).ae(8989)
    assert gegenbauer(1, -0.5, 3).ae(-3)
    assert gegenbauer(1, -1.5, 3).ae(-9)
    assert gegenbauer(1, -0.5, 3).ae(-3)
    assert gegenbauer(-0.5, -0.5, 3).ae(-2.6383553159023906245)
    assert gegenbauer(2+3j, 1-j, 3+4j).ae(14.880536623203696780 + 20.022029711598032898j)

