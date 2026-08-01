
def _pearsonr_fisher_ci(r, n, confidence_level, alternative):
    """
    Compute the confidence interval for Pearson's R.

    Fisher's transformation is used to compute the confidence interval
    (https://en.wikipedia.org/wiki/Fisher_transformation).
    """
    xp = array_namespace(r)

    ones = xp.ones_like(r)
    n = xp.asarray(n, dtype=r.dtype, device=xp_device(r))
    confidence_level = xp.asarray(confidence_level, dtype=r.dtype, device=xp_device(r))

    with np.errstate(divide='ignore', invalid='ignore'):
        zr = xp.atanh(r)
        se = xp.sqrt(1 / (n - 3))

    if alternative == "two-sided":
        h = special.ndtri(0.5 + confidence_level/2)
        zlo = zr - h*se
        zhi = zr + h*se
        rlo = xp.tanh(zlo)
        rhi = xp.tanh(zhi)
    elif alternative == "less":
        h = special.ndtri(confidence_level)
        zhi = zr + h*se
        rhi = xp.tanh(zhi)
        rlo = -ones
    else:
        # alternative == "greater":
        h = special.ndtri(confidence_level)
        zlo = zr - h*se
        rlo = xp.tanh(zlo)
        rhi = ones

    mask = (n <= 3)
    if mask.ndim == 0:
        # This is Array API legal, but Dask doesn't like it.
        mask = xp.broadcast_to(mask, rlo.shape)

    rlo = xpx.at(rlo)[mask].set(-1)
    rhi = xpx.at(rhi)[mask].set(1)

    rlo = rlo[()] if rlo.ndim == 0 else rlo
    rhi = rhi[()] if rhi.ndim == 0 else rhi
    return ConfidenceInterval(low=rlo, high=rhi)

