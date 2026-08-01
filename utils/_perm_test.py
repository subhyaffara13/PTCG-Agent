
def _perm_test(x, y, stat, reps=1000, workers=-1, random_state=None):
    r"""Helper function that calculates the p-value. See below for uses.

    Parameters
    ----------
    x, y : ndarray
        `x` and `y` have shapes ``(n, p)`` and ``(n, q)``.
    stat : float
        The sample test statistic.
    reps : int, optional
        The number of replications used to estimate the null when using the
        permutation test. The default is 1000 replications.
    workers : int or map-like callable, optional
        If `workers` is an int the population is subdivided into `workers`
        sections and evaluated in parallel (uses
        `multiprocessing.Pool <multiprocessing>`). Supply `-1` to use all cores
        available to the Process. Alternatively supply a map-like callable,
        such as `multiprocessing.Pool.map` for evaluating the population in
        parallel. This evaluation is carried out as `workers(func, iterable)`.
        Requires that `func` be pickleable.
    random_state : {None, int, `numpy.random.Generator`,
                    `numpy.random.RandomState`}, optional

        If `seed` is None (or `np.random`), the `numpy.random.RandomState`
        singleton is used.
        If `seed` is an int, a new ``RandomState`` instance is used,
        seeded with `seed`.
        If `seed` is already a ``Generator`` or ``RandomState`` instance then
        that instance is used.

    Returns
    -------
    pvalue : float
        The sample test p-value.
    null_dist : list
        The approximated null distribution.

    """
    # generate seeds for each rep (change to new parallel random number
    # capabilities in numpy >= 1.17+)
    random_state = check_random_state(random_state)
    random_states = [np.random.RandomState(rng_integers(random_state, 1 << 32,
                     size=4, dtype=np.uint32)) for _ in range(reps)]

    # parallelizes with specified workers over number of reps and set seeds
    parallelp = _ParallelP(x=x, y=y, random_states=random_states)
    with MapWrapper(workers) as mapwrapper:
        null_dist = np.array(list(mapwrapper(parallelp, range(reps))))

    # calculate p-value and significant permutation map through list
    pvalue = (1 + (null_dist >= stat).sum()) / (1 + reps)

    return pvalue, null_dist

