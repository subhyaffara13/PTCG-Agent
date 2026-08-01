
def check_pdf(distfn, arg, msg):
    # compares pdf at median with numerical derivative of cdf
    median = distfn.ppf(0.5, *arg)
    eps = 1e-6
    pdfv = distfn.pdf(median, *arg)
    if (pdfv < 1e-4) or (pdfv > 1e4):
        # avoid checking a case where pdf is close to zero or
        # huge (singularity)
        median = median + 0.1
        pdfv = distfn.pdf(median, *arg)
    cdfdiff = (distfn.cdf(median + eps, *arg) -
               distfn.cdf(median - eps, *arg))/eps/2.0
    # replace with better diff and better test (more points),
    # actually, this works pretty well
    msg += ' - cdf-pdf relationship'
    npt.assert_almost_equal(pdfv, cdfdiff, decimal=DECIMAL, err_msg=msg)

