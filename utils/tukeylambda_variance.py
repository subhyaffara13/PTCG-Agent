
def tukeylambda_variance(lam):
    """Variance of the Tukey Lambda distribution.

    Parameters
    ----------
    lam : array_like
        The lambda values at which to compute the variance.

    Returns
    -------
    v : ndarray
        The variance.  For lam < -0.5, the variance is not defined, so
        np.nan is returned.  For lam = 0.5, np.inf is returned.

    Notes
    -----
    In an interval around lambda=0, this function uses the [4,4] Pade
    approximation to compute the variance.  Otherwise it uses the standard
    formula (https://en.wikipedia.org/wiki/Tukey_lambda_distribution).  The
    Pade approximation is used because the standard formula has a removable
    discontinuity at lambda = 0, and does not produce accurate numerical
    results near lambda = 0.
    """
    lam = np.asarray(lam)
    shp = lam.shape
    lam = np.atleast_1d(lam).astype(np.float64)

    # For absolute values of lam less than threshold, use the Pade
    # approximation.
    threshold = 0.075

    # Play games with masks to implement the conditional evaluation of
    # the distribution.
    # lambda < -0.5:  var = nan
    low_mask = lam < -0.5
    # lambda == -0.5: var = inf
    neghalf_mask = lam == -0.5
    # abs(lambda) < threshold:  use Pade approximation
    small_mask = np.abs(lam) < threshold
    # else the "regular" case:  use the explicit formula.
    reg_mask = ~(low_mask | neghalf_mask | small_mask)

    # Get the 'lam' values for the cases where they are needed.
    small = lam[small_mask]
    reg = lam[reg_mask]

    # Compute the function for each case.
    v = np.empty_like(lam)
    v[low_mask] = np.nan
    v[neghalf_mask] = np.inf
    if small.size > 0:
        # Use the Pade approximation near lambda = 0.
        v[small_mask] = _tukeylambda_var_p(small) / _tukeylambda_var_q(small)
    if reg.size > 0:
        v[reg_mask] = (2.0 / reg**2) * (1.0 / (1.0 + 2 * reg) -
                                        beta(reg + 1, reg + 1))
    v = v.reshape(shp)
    return v

