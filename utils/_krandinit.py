
def _krandinit(data, k, rng, xp):
    """Returns k samples of a random variable whose parameters depend on data.

    More precisely, it returns k observations sampled from a Gaussian random
    variable whose mean and covariances are the ones estimated from the data.

    Parameters
    ----------
    data : ndarray
        Expect a rank 1 or 2 array. Rank 1 is assumed to describe 1-D
        data, rank 2 multidimensional data, in which case one
        row is one observation.
    k : int
        Number of samples to generate.
    rng : `numpy.random.Generator` or `numpy.random.RandomState`
        Random number generator.

    Returns
    -------
    x : ndarray
        A 'k' by 'N' containing the initial centroids

    """
    mu = xp.mean(data, axis=0)
    k = np.asarray(k)

    if data.ndim == 1:
        _cov = xpx.cov(data, xp=xp)
        x = rng.standard_normal(size=k)
        x = xp.asarray(x)
        x *= xp.sqrt(_cov)
    elif data.shape[1] > data.shape[0]:
        # initialize when the covariance matrix is rank deficient
        _, s, vh = xp.linalg.svd(data - mu, full_matrices=False)
        x = rng.standard_normal(size=(k, xp_size(s)))
        x = xp.asarray(x)
        sVh = s[:, None] * vh / xp.sqrt(data.shape[0] - xp.asarray(1.))
        x = x @ sVh
    else:
        _cov = xpx.atleast_nd(xpx.cov(data.T, xp=xp), ndim=2, xp=xp)

        # k rows, d cols (one row = one obs)
        # Generate k sample of a random variable ~ Gaussian(mu, cov)
        x = rng.standard_normal(size=(k, xp_size(mu)))
        x = xp.asarray(x)
        x = x @ xp.linalg.cholesky(_cov).T

    x += mu
    return x

