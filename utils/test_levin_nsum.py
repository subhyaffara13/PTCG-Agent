
def test_levin_nsum():
    mp.dps = 17

    with mp.extraprec(mp.prec):
        z = mp.mpf(10) ** (-10)
        a = mp.nsum(lambda n: n**(-(1+z)), [1, mp.inf], method = "l") - 1 / z
        assert abs(a - mp.euler) < 1e-10

    eps = mp.exp(0.8 * mp.log(mp.eps))

    a = mp.nsum(lambda n: (-1)**(n-1) / n, [1, mp.inf], method = "sidi")
    assert abs(a - mp.log(2)) < eps

    z = 2 + 1j
    f = lambda n: mp.rf(2 / mp.mpf(3), n) * mp.rf(4 / mp.mpf(3), n) * z**n / (mp.rf(1 / mp.mpf(3), n) * mp.fac(n))
    v = mp.nsum(f, [0, mp.inf], method = "levin", steps = [10 for x in xrange(1000)])
    exact = mp.hyp2f1(2 / mp.mpf(3), 4 / mp.mpf(3), 1 / mp.mpf(3), z)
    assert abs(exact - v) < eps

