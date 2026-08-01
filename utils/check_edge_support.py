
def check_edge_support(distfn, args):
    # Make sure that x=self.a and self.b are handled correctly.
    x = distfn.support(*args)
    if isinstance(distfn, stats.rv_discrete):
        x = x[0]-1, x[1]

    npt.assert_equal(distfn.cdf(x, *args), [0.0, 1.0])
    npt.assert_equal(distfn.sf(x, *args), [1.0, 0.0])

    if distfn.name not in ('skellam', 'dlaplace'):
        # with a = -inf, log(0) generates warnings
        npt.assert_equal(distfn.logcdf(x, *args), [-np.inf, 0.0])
        npt.assert_equal(distfn.logsf(x, *args), [0.0, -np.inf])

    npt.assert_equal(distfn.ppf([0.0, 1.0], *args), x)
    npt.assert_equal(distfn.isf([0.0, 1.0], *args), x[::-1])

    # out-of-bounds for isf & ppf
    npt.assert_(np.isnan(distfn.isf([-1, 2], *args)).all())
    npt.assert_(np.isnan(distfn.ppf([-1, 2], *args)).all())

