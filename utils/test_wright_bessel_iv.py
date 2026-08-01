
def test_wright_bessel_iv(b, x):
    """Test relation of wright_bessel and modified bessel function iv.

    iv(z) = (1/2*z)**v * Phi(1, v+1; 1/4*z**2).
    See https://dlmf.nist.gov/10.46.E2
    """
    if x != 0:
        v = b - 1
        wb = wright_bessel(1, v + 1, x**2 / 4.)
        # Note: iv(v, x) has precision of less than 1e-12 for some cases
        # e.g v=1-1e-6 and x=1e-06)
        assert_allclose(np.power(x / 2., v) * wb,
                        sc.iv(v, x),
                        rtol=1e-11, atol=1e-11)

