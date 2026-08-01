
def check_ppf_isf(distfn, arg, msg):
    p = np.array([0.1, 0.9])
    npt.assert_almost_equal(distfn.isf(p, *arg), distfn.ppf(1-p, *arg),
                            decimal=DECIMAL, err_msg=msg +
                            ' - ppf-isf relationship')

