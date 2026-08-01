
def check_pdf_logpdf(distfn, args, msg):
    # compares pdf at several points with the log of the pdf
    points = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    pdf = distfn.pdf(vals, *args)
    logpdf = distfn.logpdf(vals, *args)
    pdf = pdf[(pdf != 0) & np.isfinite(pdf)]
    logpdf = logpdf[np.isfinite(logpdf)]
    msg += " - logpdf-log(pdf) relationship"
    npt.assert_almost_equal(np.log(pdf), logpdf, decimal=7, err_msg=msg)

