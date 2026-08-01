
def _qmvt(m, nu, covar, low, high, rng, lattice='cbc', n_batches=10):
    """Multivariate t integration over box bounds.

    Parameters
    ----------
    m : int > n_batches
        The number of points to sample. This number will be divided into
        `n_batches` batches that apply random offsets of the sampling lattice
        for each batch in order to estimate the error.
    nu : float >= 0
        The shape parameter of the multivariate t distribution.
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
    n_samples : int
        The number of samples actually used.
    """
    sn = max(1.0, np.sqrt(nu))
    low = np.asarray(low, dtype=np.float64)
    high = np.asarray(high, dtype=np.float64)
    cho, lo, hi = _permuted_cholesky(covar, low / sn, high / sn)
    n = cho.shape[0]
    q, n_qmc_samples = _cbc_lattice(n, max(m // n_batches, 1))
    rndm = rng.random(size=(n_batches, n))
    prob, est_error, n_samples = _qmvt_inner(
        q, rndm, int(n_qmc_samples), int(n_batches), cho, lo, hi, float(nu)
    )
    return prob, est_error, n_samples

