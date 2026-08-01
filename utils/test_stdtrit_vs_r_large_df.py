
def test_stdtrit_vs_R_large_df():
    df = [1e10, 1e12, 1e120, np.inf]
    p = 0.1
    res = stdtrit(df, p)
    # R Code:
    #   options(digits=20)
    #   qt(0.1, c(1e10, 1e12, 1e120, Inf))
    res_R = [-1.2815515656292593150,
             -1.2815515655454472466,
             -1.2815515655446008125,
             -1.2815515655446008125]
    assert_allclose(res, res_R, rtol=1e-15, atol=1e-15)
    # last value should also agree with ndtri
    # actually the result from stdtrit is closer to R than ndtri,
    # so we accept a deviation of one ULP
    epsilon = np.finfo(np.float64).eps
    assert_allclose(res[3], ndtri(0.1), rtol=epsilon, atol=epsilon)

