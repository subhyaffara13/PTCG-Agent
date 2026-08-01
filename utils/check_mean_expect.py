
def check_mean_expect(distfn, arg, m, msg):
    if np.isfinite(m):
        m1 = distfn.expect(lambda x: x, arg)
        npt.assert_almost_equal(m1, m, decimal=5,
                                err_msg=msg + ' - 1st moment (expect)')

