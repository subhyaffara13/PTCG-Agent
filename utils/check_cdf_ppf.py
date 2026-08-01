
def check_cdf_ppf(distfn, arg, msg):
    values = [0.001, 0.5, 0.999]
    npt.assert_almost_equal(distfn.cdf(distfn.ppf(values, *arg), *arg),
                            values, decimal=DECIMAL, err_msg=msg +
                            ' - cdf-ppf roundtrip')


def check_cdf_ppf(distfn, arg, supp, msg):
    # supp is assumed to be an array of integers in the support of distfn
    # (but not necessarily all the integers in the support).
    # This test assumes that the PMF of any value in the support of the
    # distribution is greater than 1e-8.

    # cdf is a step function, and ppf(q) = min{k : cdf(k) >= q, k integer}
    cdf_supp = distfn.cdf(supp, *arg)
    # In very rare cases, the finite precision calculation of ppf(cdf(supp))
    # can produce an array in which an element is off by one.  We nudge the
    # CDF values down by a few ULPs help to avoid this.
    n_ulps = roundtrip_cdf_ppf_exceptions.get(distfn.name, 15)
    cdf_supp0 = cdf_supp - n_ulps*np.spacing(cdf_supp)
    npt.assert_array_equal(distfn.ppf(cdf_supp0, *arg),
                           supp, msg + '-roundtrip')
    # Repeat the same calculation, but with the CDF values decreased by 1e-8.
    npt.assert_array_equal(distfn.ppf(distfn.cdf(supp, *arg) - 1e-8, *arg),
                           supp, msg + '-roundtrip')

    if not hasattr(distfn, 'xk'):
        _a, _b = distfn.support(*arg)
        supp1 = supp[supp < _b]
        npt.assert_array_equal(distfn.ppf(distfn.cdf(supp1, *arg) + 1e-8, *arg),
                               supp1 + distfn.inc, msg + ' ppf-cdf-next')

