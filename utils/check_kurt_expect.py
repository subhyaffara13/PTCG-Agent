
def check_kurt_expect(distfn, arg, m, v, k, msg):
    if np.isfinite(k):
        m4e = distfn.expect(lambda x: np.power(x-m, 4), arg)
        npt.assert_allclose(m4e, (k + 3.) * np.power(v, 2),
                            atol=1e-5, rtol=1e-5,
                            err_msg=msg + ' - kurtosis')
    elif not np.isposinf(k):
        npt.assert_(np.isnan(k))

