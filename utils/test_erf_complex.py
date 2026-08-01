
def test_erf_complex():
    # need to increase mpmath precision for this test
    old_dps, old_prec = mpmath.mp.dps, mpmath.mp.prec
    try:
        mpmath.mp.dps = 70
        x1, y1 = np.meshgrid(np.linspace(-10, 1, 31), np.linspace(-10, 1, 11))
        x2, y2 = np.meshgrid(np.logspace(-80, .8, 31), np.logspace(-80, .8, 11))
        points = np.r_[x1.ravel(),x2.ravel()] + 1j*np.r_[y1.ravel(), y2.ravel()]

        assert_func_equal(sc.erf, lambda x: complex(mpmath.erf(x)), points,
                          vectorized=False, rtol=1e-13)
        assert_func_equal(sc.erfc, lambda x: complex(mpmath.erfc(x)), points,
                          vectorized=False, rtol=1e-13)
    finally:
        mpmath.mp.dps, mpmath.mp.prec = old_dps, old_prec

