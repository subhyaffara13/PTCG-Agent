
def check_pdf_logpdf_at_endpoints(distfn, args, msg):
    # compares pdf with the log of the pdf at the (finite) end points
    points = np.array([0, 1])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    pdf = distfn.pdf(vals, *args)
    logpdf = distfn.logpdf(vals, *args)
    pdf = pdf[(pdf != 0) & np.isfinite(pdf)]
    logpdf = logpdf[np.isfinite(logpdf)]
    msg += " - logpdf-log(pdf) relationship"
    npt.assert_almost_equal(np.log(pdf), logpdf, decimal=7, err_msg=msg)

