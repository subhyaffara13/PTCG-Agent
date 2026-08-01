
def _qmvn(m, covar, low, high, rng, lattice='cbc', n_batches=10):
    """Multivariate normal integration over box bounds.

    Parameters
    ----------
    m : int > n_batches
        The number of points to sample. This number will be divided into
        `n_batches` batches that apply random offsets of the sampling lattice
        for each batch in order to estimate the error.
    covar : (n, n) float array
        Possibly singular, positive semidefinite symmetric covariance matrix.
    low, high : (n,) float array
        The low and high integration bounds.
    rng : Generator, optional
        default_rng(), yada, yada
    lattice : 'cbc' or callable
        The type of lattice rule to use to construct the integration points.
    n_batches : int > 0, optional
        The number of QMC batches to apply.

    Returns
    -------
    prob : float
        The estimated probability mass within the bounds.
    est_error : float
        3 times the standard error of the batch estimates.
    """
    cho, lo, hi = _permuted_cholesky(covar, low, high)
    if not cho.flags.c_contiguous:
        # qmvn_inner expects contiguous buffers
        cho = cho.copy()

    n = cho.shape[0]
    q, n_qmc_samples = _cbc_lattice(n - 1, max(m // n_batches, 1))
    rndm = rng.random(size=(n_batches, n))

    prob, est_error, n_samples = _qmvn_inner(
        q, rndm, int(n_qmc_samples), int(n_batches), cho, lo, hi
    )
    return prob, est_error, n_samples

