
def kmeans2(data, k, iter=10, thresh=1e-5, minit='random',
            missing='warn', check_finite=True, *, rng=None):
    """
    Classify a set of observations into k clusters using the k-means algorithm.

    The algorithm attempts to minimize the Euclidean distance between
    observations and centroids. Several initialization methods are
    included.

    Parameters
    ----------
    data : ndarray
        A 'M' by 'N' array of 'M' observations in 'N' dimensions or a length
        'M' array of 'M' 1-D observations.
    k : int or ndarray
        The number of clusters to form as well as the number of
        centroids to generate. If `minit` initialization string is
        'matrix', or if an ndarray is given instead, it is
        interpreted as initial cluster to use instead.
    iter : int, optional
        Number of iterations of the k-means algorithm to run. Note
        that this differs in meaning from the iters parameter to
        the kmeans function.
    thresh : float, optional
        (not used yet)
    minit : str, optional
        Method for initialization. Available methods are 'random',
        'points', '++' and 'matrix':

        'random': generate k centroids from a Gaussian with mean and
        variance estimated from the data.

        'points': choose k observations (rows) at random from data for
        the initial centroids.

        '++': choose k observations accordingly to the kmeans++ method
        (careful seeding)

        'matrix': interpret the k parameter as a k by M (or length k
        array for 1-D data) array of initial centroids.
    missing : str, optional
        Method to deal with empty clusters. Available methods are
        'warn' and 'raise':

        'warn': give a warning and continue.

        'raise': raise a ClusterError and terminate the algorithm.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
        Default: True
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.

    Returns
    -------
    centroid : ndarray
        A 'k' by 'N' array of centroids found at the last iteration of
        k-means.
    label : ndarray
        label[i] is the code or index of the centroid the
        ith observation is closest to.

    See Also
    --------
    kmeans

    References
    ----------
    .. [1] D. Arthur and S. Vassilvitskii, "k-means++: the advantages of
       careful seeding", Proceedings of the Eighteenth Annual ACM-SIAM Symposium
       on Discrete Algorithms, 2007.

    Examples
    --------
    >>> from scipy.cluster.vq import kmeans2
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    Create z, an array with shape (100, 2) containing a mixture of samples
    from three multivariate normal distributions.

    >>> rng = np.random.default_rng()
    >>> a = rng.multivariate_normal([0, 6], [[2, 1], [1, 1.5]], size=45)
    >>> b = rng.multivariate_normal([2, 0], [[1, -1], [-1, 3]], size=30)
    >>> c = rng.multivariate_normal([6, 4], [[5, 0], [0, 1.2]], size=25)
    >>> z = np.concatenate((a, b, c))
    >>> rng.shuffle(z)

    Compute three clusters.

    >>> centroid, label = kmeans2(z, 3, minit='points')
    >>> centroid
    array([[ 2.22274463, -0.61666946],  # may vary
           [ 0.54069047,  5.86541444],
           [ 6.73846769,  4.01991898]])

    How many points are in each cluster?

    >>> counts = np.bincount(label)
    >>> counts
    array([29, 51, 20])  # may vary

    Plot the clusters.

    >>> w0 = z[label == 0]
    >>> w1 = z[label == 1]
    >>> w2 = z[label == 2]
    >>> plt.plot(w0[:, 0], w0[:, 1], 'o', alpha=0.5, label='cluster 0')
    >>> plt.plot(w1[:, 0], w1[:, 1], 'd', alpha=0.5, label='cluster 1')
    >>> plt.plot(w2[:, 0], w2[:, 1], 's', alpha=0.5, label='cluster 2')
    >>> plt.plot(centroid[:, 0], centroid[:, 1], 'k*', label='centroids')
    >>> plt.axis('equal')
    >>> plt.legend(shadow=True)
    >>> plt.show()

    """
    if int(iter) < 1:
        raise ValueError(f"Invalid iter ({iter}), must be a positive integer.")
    try:
        miss_meth = _valid_miss_meth[missing]
    except KeyError as e:
        raise ValueError(f"Unknown missing method {missing!r}") from e

    if isinstance(k, int):
        xp = array_namespace(data)
    else:
        xp = array_namespace(data, k)
    data = _asarray(data, xp=xp, check_finite=check_finite)
    code_book = xp_copy(k, xp=xp)
    if data.ndim == 1:
        d = 1
    elif data.ndim == 2:
        d = data.shape[1]
    else:
        raise ValueError("Input of rank > 2 is not supported.")

    if xp_size(data) < 1 or xp_size(code_book) < 1:
        raise ValueError("Empty input is not supported.")

    # If k is not a single value, it should be compatible with data's shape
    if minit == 'matrix' or xp_size(code_book) > 1:
        if data.ndim != code_book.ndim:
            raise ValueError("k array doesn't match data rank")
        nc = code_book.shape[0]
        if data.ndim > 1 and code_book.shape[1] != d:
            raise ValueError("k array doesn't match data dimension")
    else:
        nc = int(code_book)

        if nc < 1:
            raise ValueError(
                f"Cannot ask kmeans2 for {nc} clusters (k was {code_book})"
            )
        elif nc != code_book:
            warnings.warn("k was not an integer, was converted.", stacklevel=2)

        try:
            init_meth = _valid_init_meth[minit]
        except KeyError as e:
            raise ValueError(f"Unknown init method {minit!r}") from e
        else:
            rng = check_random_state(rng)
            code_book = init_meth(data, code_book, rng, xp)

    data = np.asarray(data)
    code_book = np.asarray(code_book)
    for _ in range(iter):
        # Compute the nearest neighbor for each obs using the current code book
        label = vq(data, code_book, check_finite=check_finite)[0]
        # Update the code book by computing centroids
        new_code_book, has_members = _vq.update_cluster_means(data, label, nc)
        if not has_members.all():
            miss_meth()
            # Set the empty clusters to their previous positions
            new_code_book[~has_members] = code_book[~has_members]
        code_book = new_code_book

    return xp.asarray(code_book), xp.asarray(label)

