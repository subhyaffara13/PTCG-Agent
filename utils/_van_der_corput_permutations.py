
def _van_der_corput_permutations(
    base: IntNumber, *, rng: SeedType = None
) -> np.ndarray:
    """Permutations for scrambling a Van der Corput sequence.

    Parameters
    ----------
    base : int
        Base of the sequence.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.

        .. versionchanged:: 1.15.0

            As part of the `SPEC-007 <https://scientific-python.org/specs/spec-0007/>`_
            transition from use of `numpy.random.RandomState` to
            `numpy.random.Generator`, this keyword was changed from `seed` to
            `rng`. During the transition, the behavior documented above is not
            accurate; see `check_random_state` for actual behavior. After the
            transition, this admonition can be removed.

    Returns
    -------
    permutations : array_like
        Permutation indices.

    Notes
    -----
    In Algorithm 1 of Owen 2017, a permutation of `np.arange(base)` is
    created for each positive integer `k` such that ``1 - base**-k < 1``
    using floating-point arithmetic. For double precision floats, the
    condition ``1 - base**-k < 1`` can also be written as ``base**-k >
    2**-54``, which makes it more apparent how many permutations we need
    to create.
    """
    rng = check_random_state(rng)
    count = math.ceil(54 / math.log2(base)) - 1
    permutations = np.repeat(np.arange(base)[None], count, axis=0)
    for perm in permutations:
        rng.shuffle(perm)

    return permutations

