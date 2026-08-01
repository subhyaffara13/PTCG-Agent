
def test_riemann_zeta_complex(z, desired, rtol):
    assert_allclose(sc.zeta(z), desired, rtol=rtol)

