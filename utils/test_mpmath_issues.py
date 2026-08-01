
def test_mpmath_issues():
    from mpmath.libmp.libmpf import _normalize
    import mpmath.libmp as mlib
    rnd = mlib.round_nearest
    mpf = (0, int(0), -123, -1, 53, rnd)  # nan
    assert _normalize(mpf, 53) != (0, int(0), 0, 0)
    mpf = (0, int(0), -456, -2, 53, rnd)  # +inf
    assert _normalize(mpf, 53) != (0, int(0), 0, 0)
    mpf = (1, int(0), -789, -3, 53, rnd)  # -inf
    assert _normalize(mpf, 53) != (0, int(0), 0, 0)

    from mpmath.libmp.libmpf import fnan
    assert mlib.mpf_eq(fnan, fnan)

