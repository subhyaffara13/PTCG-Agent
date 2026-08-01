
def _argus_phi(chi):
    """
    Utility function for the argus distribution used in the pdf, sf and
    moment calculation.
    Note that for all x > 0:
    gammainc(1.5, x**2/2) = 2 * (_norm_cdf(x) - x * _norm_pdf(x) - 0.5).
    This can be verified directly by noting that the cdf of Gamma(1.5) can
    be written as erf(sqrt(x)) - 2*sqrt(x)*exp(-x)/sqrt(Pi).
    We use gammainc instead of the usual definition because it is more precise
    for small chi.
    """
    return sc.gammainc(1.5, chi**2/2) / 2

