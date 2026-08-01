
def tukeylambda_kurtosis(lam):
    """Kurtosis of the Tukey Lambda distribution.

    Parameters
    ----------
    lam : array_like
        The lambda values at which to compute the variance.

    Returns
    -------
    v : ndarray
        The variance.  For lam < -0.25, the variance is not defined, so
        np.nan is returned.  For lam = 0.25, np.inf is returned.

    """
    lam = np.asarray(lam)
    shp = lam.shape
    lam = np.atleast_1d(lam).astype(np.float64)

    # For absolute values of lam less than threshold, use the Pade
    # approximation.
    threshold = 0.055

    # Use masks to implement the conditional evaluation of the kurtosis.
    # lambda < -0.25:  kurtosis = nan
    low_mask = lam < -0.25
    # lambda == -0.25: kurtosis = inf
    negqrtr_mask = lam == -0.25
    # lambda near 0:  use Pade approximation
    small_mask = np.abs(lam) < threshold
    # else the "regular" case:  use the explicit formula.
    reg_mask = ~(low_mask | negqrtr_mask | small_mask)

    # Get the 'lam' values for the cases where they are needed.
    small = lam[small_mask]
    reg = lam[reg_mask]

    # Compute the function for each case.
    k = np.empty_like(lam)
    k[low_mask] = np.nan
    k[negqrtr_mask] = np.inf
    if small.size > 0:
        k[small_mask] = _tukeylambda_kurt_p(small) / _tukeylambda_kurt_q(small)
    if reg.size > 0:
        numer = (1.0 / (4 * reg + 1) - 4 * beta(3 * reg + 1, reg + 1) +
                 3 * beta(2 * reg + 1, 2 * reg + 1))
        denom = 2 * (1.0/(2 * reg + 1) - beta(reg + 1, reg + 1))**2
        k[reg_mask] = numer / denom - 3

    # The return value will be a numpy array; resetting the shape ensures that
    # if `lam` was a scalar, the return value is a 0-d array.
    k = k.reshape(shp)
    return k

