
def _cholesky_invwishart_rvs(
    df: float, scale: np.ndarray, size: int, random_state: np.random.Generator
) -> np.ndarray:
    r"""Samples the lower Cholesky factor of a matrix following an inverse
    Wishart distribution.

    Notes
    -----
    Intended to be used *as a step in the process* for computing random variates
    of a matrix t distribution :math:`\mathcal{T}_{m,n}` by appealing to its
    alternative form as a matrix mixture
    .. math::
        \mathcal{T}_{m,n}( \mathrm{df}, \mathrm{M}, \Sigma, \Omega )
        = \mathcal{N}_{m,n}(
            \mathrm{M},
            \mathcal{W}^{-1}_m(\mathrm{df} + m - 1, \Sigma),
            \Omega
            )
        = \mathcal{N}_{m,n}(
            \mathrm{M},
            \Sigma,
            \mathcal{W}^{-1}_n(\mathrm{df} - n + 1, \Omega)
            )
    where :math:`\mathcal{N}_{m,n}` is a matrix normal distribution
    and :math:`\mathcal{W}^{-1}_d` is an inverse Wishart distribution.
    Accordingly, the degrees of freedom adjustment
    :math:`\mathrm{df} \to \mathrm{df} + d - 1`
    occurrs in the scope of this function.
    """
    df_iw = df + scale.shape[0] - 1
    iw_samples = scipy.stats.invwishart.rvs(df_iw, scale, size, random_state)
    if size == 1:
        iw_samples = iw_samples[np.newaxis, ...]
    chol_samples = np.empty_like(iw_samples)
    for idx in range(size):
        chol_samples[idx] = scipy.linalg.cholesky(
            iw_samples[idx], lower=True, check_finite=False
        ).reshape(iw_samples.shape[1:])
    return chol_samples.reshape((size, *scale.shape))

