
def test_root():
    from sympy.abc import x
    n = Symbol('n', integer=True)
    k = Symbol('k', integer=True)

    assert root(2, 2) == sqrt(2)
    assert root(2, 1) == 2
    assert root(2, 3) == 2**Rational(1, 3)
    assert root(2, 3) == cbrt(2)
    assert root(2, -5) == 2**Rational(4, 5)/2

    assert root(-2, 1) == -2

    assert root(-2, 2) == sqrt(2)*I
    assert root(-2, 1) == -2

    assert root(x, 2) == sqrt(x)
    assert root(x, 1) == x
    assert root(x, 3) == x**Rational(1, 3)
    assert root(x, 3) == cbrt(x)
    assert root(x, -5) == x**Rational(-1, 5)

    assert root(x, n) == x**(1/n)
    assert root(x, -n) == x**(-1/n)

    assert root(x, n, k) == (-1)**(2*k/n)*x**(1/n)


def test_root():
    mp.dps = 30
    random.seed(1)
    a = random.randint(0, 10000)
    p = a*a*a
    r = nthroot(mpf(p), 3)
    assert r == a
    for n in range(4, 10):
        p = p*a
        assert nthroot(mpf(p), n) == a
    mp.dps = 40
    for n in range(10, 5000, 100):
        for a in [random.random()*10000, random.random()*10**100]:
            r = nthroot(a, n)
            r1 = pow(a, mpf(1)/n)
            assert r.ae(r1)
            r = nthroot(a, -n)
            r1 = pow(a, -mpf(1)/n)
            assert r.ae(r1)
    # XXX: this is broken right now
    # tests for nthroot rounding
    for rnd in ['nearest', 'up', 'down']:
        mp.rounding = rnd
        for n in [-5, -3, 3, 5]:
            prec = 50
            for i in range(10):
                mp.prec = prec
                a = rand()
                mp.prec = 2*prec
                b = a**n
                mp.prec = prec
                r = nthroot(b, n)
                assert r == a
    mp.dps = 30
    for n in range(3, 21):
        a = (random.random() + j*random.random())
        assert nthroot(a, n).ae(pow(a, mpf(1)/n))
        assert mpc_ae(nthroot(a, n), pow(a, mpf(1)/n))
        a = (random.random()*10**100 + j*random.random())
        r = nthroot(a, n)
        mp.dps += 4
        r1 = pow(a, mpf(1)/n)
        mp.dps -= 4
        assert r.ae(r1)
        assert mpc_ae(r, r1, eps)
        r = nthroot(a, -n)
        mp.dps += 4
        r1 = pow(a, -mpf(1)/n)
        mp.dps -= 4
        assert r.ae(r1)
        assert mpc_ae(r, r1, eps)
    mp.dps = 15
    assert nthroot(4, 1) == 4
    assert nthroot(4, 0) == 1
    assert nthroot(4, -1) == 0.25
    assert nthroot(inf, 1) == inf
    assert nthroot(inf, 2) == inf
    assert nthroot(inf, 3) == inf
    assert nthroot(inf, -1) == 0
    assert nthroot(inf, -2) == 0
    assert nthroot(inf, -3) == 0
    assert nthroot(j, 1) == j
    assert nthroot(j, 0) == 1
    assert nthroot(j, -1) == -j
    assert isnan(nthroot(nan, 1))
    assert isnan(nthroot(nan, 0))
    assert isnan(nthroot(nan, -1))
    assert isnan(nthroot(inf, 0))
    assert root(2,3) == nthroot(2,3)
    assert root(16,4,0) == 2
    assert root(16,4,1) == 2j
    assert root(16,4,2) == -2
    assert root(16,4,3) == -2j
    assert root(16,4,4) == 2
    assert root(-125,3,1) == -5

