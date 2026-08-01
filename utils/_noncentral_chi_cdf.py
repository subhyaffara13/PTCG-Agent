
def _noncentral_chi_cdf(x, df, nc, dps=None):
    if dps is None:
        dps = mpmath.mp.dps
    x, df, nc = mpmath.mpf(x), mpmath.mpf(df), mpmath.mpf(nc)
    with mpmath.workdps(dps):
        res = mpmath.quad(lambda t: _noncentral_chi_pdf(t, df, nc), [0, x])
        return res

