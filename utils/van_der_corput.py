
def van_der_corput(
        n: IntNumber,
        base: IntNumber = 2,
        *,
        start_index: IntNumber = 0,
        scramble: bool = False,
        permutations: "npt.ArrayLike | None" = None,
        rng: SeedType = None,
        workers: IntNumber = 1) -> np.ndarray:
    """Van der Corput sequence.

    Pseudo-random number generator based on a b-adic expansion.

    Scrambling uses permutations of the remainders (see [1]_). Multiple
    permutations are applied to construct a point. The sequence of
    permutations has to be the same for all points of the sequence.

    Parameters
    ----------
    n : int
        Number of element of the sequence.
    base : int, optional
        Base of the sequence. Default is 2.
    start_index : int, optional
        Index to start the sequence from. Default is 0.
    scramble : bool, optional
        If True, use Owen scrambling. Otherwise no scrambling is done.
        Default is True.
    permutations : array_like, optional
        Permutations used for scrambling.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.
    workers : int, optional
        Number of workers to use for parallel processing. If -1 is
        given all CPU threads are used. Default is 1.

    Returns
    -------
    sequence : list (n,)
        Sequence of Van der Corput.

    References
    ----------
    .. [1] A. B. Owen. "A randomized Halton algorithm in R",
       :arxiv:`1706.02808`, 2017.

    """
    if base < 2:
        raise ValueError("'base' must be at least 2")

    if scramble:
        if permutations is None:
            permutations = _van_der_corput_permutations(
                base=base, rng=rng
            )
        else:
            permutations = np.asarray(permutations)

        permutations = permutations.astype(np.int64)
        return _cy_van_der_corput_scrambled(n, base, start_index,
                                            permutations, workers)

    else:
        return _cy_van_der_corput(n, base, start_index, workers)

