
def _kpp(data, k, rng, xp):
    """ Picks k points in the data based on the kmeans++ method.

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
    init : ndarray
        A 'k' by 'N' containing the initial centroids.

    References
    ----------
    .. [1] D. Arthur and S. Vassilvitskii, "k-means++: the advantages of
       careful seeding", Proceedings of the Eighteenth Annual ACM-SIAM Symposium
       on Discrete Algorithms, 2007.
    """

    ndim = len(data.shape)
    if ndim == 1:
        data = data[:, None]

    dims = data.shape[1]

    init = xp.empty((int(k), dims))

    for i in range(k):
        if i == 0:
            data_idx = rng_integers(rng, data.shape[0])
        else:
            D2 = cdist(init[:i,:], data, metric='sqeuclidean').min(axis=0)
            probs = D2/D2.sum()
            cumprobs = probs.cumsum()
            r = rng.uniform()
            cumprobs = np.asarray(cumprobs)
            data_idx = int(np.searchsorted(cumprobs, r))

        init = xpx.at(init)[i, :].set(data[data_idx, :])

    if ndim == 1:
        init = init[:, 0]
    return init

