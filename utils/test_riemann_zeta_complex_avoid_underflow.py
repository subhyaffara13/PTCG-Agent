
def test_riemann_zeta_complex_avoid_underflow(z, desired, rtol):
    assert_allclose(sc.zeta(z), desired, rtol=rtol)

