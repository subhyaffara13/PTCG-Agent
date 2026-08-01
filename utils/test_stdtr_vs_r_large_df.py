
def test_stdtr_vs_R_large_df():
    df = [1e10, 1e12, 1e120, np.inf]
    t = 1.
    res = stdtr(df, t)
    # R Code:
    #   options(digits=20)
    #   pt(1., c(1e10, 1e12, 1e120, Inf))
    res_R = [0.84134474605644460343,
             0.84134474606842180044,
             0.84134474606854281475,
             0.84134474606854292578]
    assert_allclose(res, res_R, rtol=1e-15)
    # last value should also agree with ndtr
    assert_equal(res[3], ndtr(1.))

