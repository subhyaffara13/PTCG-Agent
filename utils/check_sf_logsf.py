
def check_sf_logsf(distfn, args, msg):
    # compares sf at several points with the log of the sf
    points = np.array([0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    sf = distfn.sf(vals, *args)
    logsf = distfn.logsf(vals, *args)
    sf = sf[sf != 0]
    logsf = logsf[np.isfinite(logsf)]
    msg += " - logsf-log(sf) relationship"
    npt.assert_almost_equal(np.log(sf), logsf, decimal=7, err_msg=msg)

