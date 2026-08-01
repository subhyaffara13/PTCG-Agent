
def maxdists(Z):
    """
    Return the maximum distance between any non-singleton cluster.

    Parameters
    ----------
    Z : ndarray
        The hierarchical clustering encoded as a matrix. See
        ``linkage`` for more information.

    Returns
    -------
    maxdists : ndarray
        A ``(n-1)`` sized numpy array of doubles; ``MD[i]`` represents
        the maximum distance between any cluster (including
        singletons) below and including the node with index i. More
        specifically, ``MD[i] = Z[Q(i)-n, 2].max()`` where ``Q(i)`` is the
        set of all node indices below and including node i.

    See Also
    --------
    linkage : for a description of what a linkage matrix is.
    is_monotonic : for testing for monotonicity of a linkage matrix.

    Examples
    --------
    >>> from scipy.cluster.hierarchy import median, maxdists
    >>> from scipy.spatial.distance import pdist

    Given a linkage matrix ``Z``, `scipy.cluster.hierarchy.maxdists`
    computes for each new cluster generated (i.e., for each row of the linkage
    matrix) what is the maximum distance between any two child clusters.

    Due to the nature of hierarchical clustering, in many cases this is going
    to be just the distance between the two child clusters that were merged
    to form the current one - that is, Z[:,2].

    However, for non-monotonic cluster assignments such as
    `scipy.cluster.hierarchy.median` clustering this is not always the
    case: There may be cluster formations were the distance between the two
    clusters merged is smaller than the distance between their children.

    We can see this in an example:

    >>> X = [[0, 0], [0, 1], [1, 0],
    ...      [0, 4], [0, 3], [1, 4],
    ...      [4, 0], [3, 0], [4, 1],
    ...      [4, 4], [3, 4], [4, 3]]

    >>> Z = median(pdist(X))
    >>> Z
    array([[ 0.        ,  1.        ,  1.        ,  2.        ],
           [ 3.        ,  4.        ,  1.        ,  2.        ],
           [ 9.        , 10.        ,  1.        ,  2.        ],
           [ 6.        ,  7.        ,  1.        ,  2.        ],
           [ 2.        , 12.        ,  1.11803399,  3.        ],
           [ 5.        , 13.        ,  1.11803399,  3.        ],
           [ 8.        , 15.        ,  1.11803399,  3.        ],
           [11.        , 14.        ,  1.11803399,  3.        ],
           [18.        , 19.        ,  3.        ,  6.        ],
           [16.        , 17.        ,  3.5       ,  6.        ],
           [20.        , 21.        ,  3.25      , 12.        ]])
    >>> maxdists(Z)
    array([1.        , 1.        , 1.        , 1.        , 1.11803399,
           1.11803399, 1.11803399, 1.11803399, 3.        , 3.5       ,
           3.5       ])

    Note that while the distance between the two clusters merged when creating the
    last cluster is 3.25, there are two children (clusters 16 and 17) whose distance
    is larger (3.5). Thus, `scipy.cluster.hierarchy.maxdists` returns 3.5 in
    this case.

    """
    xp = array_namespace(Z)
    Z = _asarray(Z, order='C', dtype=xp.float64, xp=xp)
    _is_valid_linkage(Z, throw=True, name='Z', xp=xp)

    def cy_maxdists(Z, validate):
        if validate:
            _is_valid_linkage(Z, throw=True, name='Z', xp=np)
        MD = np.zeros((Z.shape[0],))
        _hierarchy.get_max_dist_for_each_cluster(Z, MD, Z.shape[0] + 1)
        return MD

    return xpx.lazy_apply(cy_maxdists, Z, validate=is_lazy_array(Z),
                          shape=(Z.shape[0], ), dtype=xp.float64,
                          as_numpy=True, xp=xp)

