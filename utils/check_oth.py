
def check_oth(distfn, arg, supp, msg):
    # checking other methods of distfn
    npt.assert_allclose(distfn.sf(supp, *arg), 1. - distfn.cdf(supp, *arg),
                        atol=1e-10, rtol=1e-10)

    q = np.linspace(0.01, 0.99, 20)
    npt.assert_allclose(distfn.isf(q, *arg), distfn.ppf(1. - q, *arg),
                        atol=1e-10, rtol=1e-10)

    median_sf = distfn.isf(0.5, *arg)
    npt.assert_(distfn.sf(median_sf - 1, *arg) > 0.5)
    npt.assert_(distfn.cdf(median_sf + 1, *arg) > 0.5)

