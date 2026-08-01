
def test_riemann_zeta_avoid_overflow():
    s = -260.00000000001
    desired = -5.6966307844402683127e+297  # Computed with Mpmath
    assert_allclose(sc.zeta(s), desired, atol=0, rtol=5e-14)

