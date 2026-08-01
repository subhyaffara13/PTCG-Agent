
def test_zeta_near_1():
    # Test for a former bug in mpf_zeta and mpc_zeta
    mp.dps = 15
    s1 = fadd(1, '1e-10', exact=True)
    s2 = fadd(1, '-1e-10', exact=True)
    s3 = fadd(1, '1e-10j', exact=True)
    assert zeta(s1).ae(1.000000000057721566490881444e10)
    assert zeta(s2).ae(-9.99999999942278433510574872e9)
    z = zeta(s3)
    assert z.real.ae(0.57721566490153286060)
    assert z.imag.ae(-9.9999999999999999999927184e9)
    mp.dps = 30
    s1 = fadd(1, '1e-50', exact=True)
    s2 = fadd(1, '-1e-50', exact=True)
    s3 = fadd(1, '1e-50j', exact=True)
    assert zeta(s1).ae('1e50')
    assert zeta(s2).ae('-1e50')
    z = zeta(s3)
    assert z.real.ae('0.57721566490153286060651209008240243104215933593992')
    assert z.imag.ae('-1e50')

