
def test_sn_cn_dn_complex():
    mp.dps = 30
    # N[JacobiSN[1/4 + I/8, 1/3 + I/7], 35] in Mathematica
    res = mpf('0.2495674401066275492326652143537') + \
          mpf('0.12017344422863833381301051702823') * j
    u = mpf(1)/4 + j/8
    m = mpf(1)/3 + j/7
    r = jsn(u, m)
    assert(mpc_ae(r, res))

    #N[JacobiCN[1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('0.9762691700944007312693721148331') - \
          mpf('0.0307203994181623243583169154824')*j
    r = jcn(u, m)
    #assert r.real.ae(res.real)
    #assert r.imag.ae(res.imag)
    assert(mpc_ae(r, res))

    #N[JacobiDN[1/4 + I/8, 1/3 + I/7], 35]
    res = mpf('0.99639490163039577560547478589753039') - \
          mpf('0.01346296520008176393432491077244994')*j
    r = jdn(u, m)
    assert(mpc_ae(r, res))
    mp.dps = 15

