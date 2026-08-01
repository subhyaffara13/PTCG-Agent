
def test_levin_3():
    mp.dps = 17
    z=mp.mpf(2)
    eps = mp.mpf(mp.eps)
    with mp.extraprec(7*mp.prec):  # we need copious amount of precision to sum this highly divergent series
        L = mp.levin(method = "levin", variant = "t")
        n, s = 0, 0
        while 1:
            s += (-z)**n * mp.fac(4 * n) / (mp.fac(n) * mp.fac(2 * n) * (4 ** n))
            n += 1
            v, e = L.step_psum(s)
            if e < eps:
                break
            if n > 1000: raise RuntimeError("iteration limit exceeded")
    eps = mp.exp(0.8 * mp.log(eps))
    exact = mp.quad(lambda x: mp.exp( -x * x / 2 - z * x ** 4), [0,mp.inf]) * 2 / mp.sqrt(2 * mp.pi)
    # there is also a symbolic expression for the integral:
    #   exact = mp.exp(mp.one / (32 * z)) * mp.besselk(mp.one / 4, mp.one / (32 * z)) / (4 * mp.sqrt(z * mp.pi))
    err = abs(v - exact)
    assert err < eps
    w = mp.nsum(lambda n: (-z)**n * mp.fac(4 * n) / (mp.fac(n) * mp.fac(2 * n) * (4 ** n)), [0, mp.inf], method = "levin", levin_variant = "t", workprec = 8*mp.prec, steps = [2] + [1 for x in xrange(1000)])
    err = abs(v - w)
    assert err < eps

