
def test_loggamma():
    raises(TypeError, lambda: loggamma(2, 3))
    raises(ArgumentIndexError, lambda: loggamma(x).fdiff(2))

    assert loggamma(-1) is oo
    assert loggamma(-2) is oo
    assert loggamma(0) is oo
    assert loggamma(1) == 0
    assert loggamma(2) == 0
    assert loggamma(3) == log(2)
    assert loggamma(4) == log(6)

    n = Symbol("n", integer=True, positive=True)
    assert loggamma(n) == log(gamma(n))
    assert loggamma(-n) is oo
    assert loggamma(n/2) == log(2**(-n + 1)*sqrt(pi)*gamma(n)/gamma(n/2 + S.Half))

    assert loggamma(oo) is oo
    assert loggamma(-oo) is zoo
    assert loggamma(I*oo) is zoo
    assert loggamma(-I*oo) is zoo
    assert loggamma(zoo) is zoo
    assert loggamma(nan) is nan

    L = loggamma(Rational(16, 3))
    E = -5*log(3) + loggamma(Rational(1, 3)) + log(4) + log(7) + log(10) + log(13)
    assert expand_func(L).doit() == E
    assert L.n() == E.n()

    L = loggamma(Rational(19, 4))
    E = -4*log(4) + loggamma(Rational(3, 4)) + log(3) + log(7) + log(11) + log(15)
    assert expand_func(L).doit() == E
    assert L.n() == E.n()

    L = loggamma(Rational(23, 7))
    E = -3*log(7) + log(2) + loggamma(Rational(2, 7)) + log(9) + log(16)
    assert expand_func(L).doit() == E
    assert L.n() == E.n()

    L = loggamma(Rational(19, 4) - 7)
    E = -log(9) - log(5) + loggamma(Rational(3, 4)) + 3*log(4) - 3*I*pi
    assert expand_func(L).doit() == E
    assert L.n() == E.n()

    L = loggamma(Rational(23, 7) - 6)
    E = -log(19) - log(12) - log(5) + loggamma(Rational(2, 7)) + 3*log(7) - 3*I*pi
    assert expand_func(L).doit() == E
    assert L.n() == E.n()

    assert loggamma(x).diff(x) == polygamma(0, x)
    s1 = loggamma(1/(x + sin(x)) + cos(x)).nseries(x, n=4)
    s2 = (-log(2*x) - 1)/(2*x) - log(x/pi)/2 + (4 - log(2*x))*x/24 + O(x**2) + \
        log(x)*x**2/2
    assert (s1 - s2).expand(force=True).removeO() == 0
    s1 = loggamma(1/x).series(x)
    s2 = (1/x - S.Half)*log(1/x) - 1/x + log(2*pi)/2 + \
        x/12 - x**3/360 + x**5/1260 + O(x**7)
    assert ((s1 - s2).expand(force=True)).removeO() == 0

    assert loggamma(x).rewrite('intractable') == log(gamma(x))

    s1 = loggamma(x).series(x).cancel()
    assert s1 == -log(x) - EulerGamma*x + pi**2*x**2/12 + x**3*polygamma(2, 1)/6 + \
        pi**4*x**4/360 + x**5*polygamma(4, 1)/120 + O(x**6)
    assert s1 == loggamma(x).rewrite('intractable').series(x).cancel()

    assert conjugate(loggamma(x)) == loggamma(conjugate(x))
    assert conjugate(loggamma(0)) is oo
    assert conjugate(loggamma(1)) == loggamma(conjugate(1))
    assert conjugate(loggamma(-oo)) == conjugate(zoo)

    assert loggamma(Symbol('v', positive=True)).is_real is True
    assert loggamma(Symbol('v', zero=True)).is_real is False
    assert loggamma(Symbol('v', negative=True)).is_real is False
    assert loggamma(Symbol('v', nonpositive=True)).is_real is False
    assert loggamma(Symbol('v', nonnegative=True)).is_real is None
    assert loggamma(Symbol('v', imaginary=True)).is_real is None
    assert loggamma(Symbol('v', real=True)).is_real is None
    assert loggamma(Symbol('v')).is_real is None

    assert loggamma(S.Half).is_real is True
    assert loggamma(0).is_real is False
    assert loggamma(Rational(-1, 2)).is_real is False
    assert loggamma(I).is_real is None
    assert loggamma(2 + 3*I).is_real is None

    def tN(N, M):
        assert loggamma(1/x)._eval_nseries(x, n=N).getn() == M
    tN(0, 0)
    tN(1, 1)
    tN(2, 2)
    tN(3, 3)
    tN(4, 4)
    tN(5, 5)

