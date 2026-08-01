
def check_cdf_logcdf(distfn, args, msg):
    # compares cdf at several points with the log of the cdf
    points = np.array([0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    cdf = distfn.cdf(vals, *args)
    logcdf = distfn.logcdf(vals, *args)
    cdf = cdf[cdf != 0]
    logcdf = logcdf[np.isfinite(logcdf)]
    msg += " - logcdf-log(cdf) relationship"
    npt.assert_almost_equal(np.log(cdf), logcdf, decimal=7, err_msg=msg)

