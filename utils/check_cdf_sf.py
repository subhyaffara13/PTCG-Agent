
def check_cdf_sf(distfn, arg, msg):
    npt.assert_almost_equal(distfn.cdf([0.1, 0.9], *arg),
                            1.0 - distfn.sf([0.1, 0.9], *arg),
                            decimal=DECIMAL, err_msg=msg +
                            ' - cdf-sf relationship')

