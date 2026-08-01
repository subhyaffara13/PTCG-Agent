
def check_skew_expect(distfn, arg, m, v, s, msg):
    if np.isfinite(s):
        m3e = distfn.expect(lambda x: np.power(x-m, 3), arg)
        npt.assert_almost_equal(m3e, s * np.power(v, 1.5),
                                decimal=5, err_msg=msg + ' - skew')
    else:
        npt.assert_(np.isnan(s))

