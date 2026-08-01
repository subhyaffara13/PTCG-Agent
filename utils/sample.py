
def sample(expr, condition=None, size=(), library='scipy',
           numsamples=1, seed=None, **kwargs):
    """
    A realization of the random expression.

    Parameters
    ==========

    expr : Expression of random variables
        Expression from which sample is extracted
    condition : Expr containing RandomSymbols
        A conditional expression
    size : int, tuple
        Represents size of each sample in numsamples
    library : str
        - 'scipy' : Sample using scipy
        - 'numpy' : Sample using numpy
        - 'pymc'  : Sample using PyMC

        Choose any of the available options to sample from as string,
        by default is 'scipy'
    numsamples : int
        Number of samples, each with size as ``size``.

        .. deprecated:: 1.9

        The ``numsamples`` parameter is deprecated and is only provided for
        compatibility with v1.8. Use a list comprehension or an additional
        dimension in ``size`` instead. See
        :ref:`deprecated-sympy-stats-numsamples` for details.

    seed :
        An object to be used as seed by the given external library for sampling `expr`.
        Following is the list of possible types of object for the supported libraries,

        - 'scipy': int, numpy.random.RandomState, numpy.random.Generator
        - 'numpy': int, numpy.random.RandomState, numpy.random.Generator
        - 'pymc': int

        Optional, by default None, in which case seed settings
        related to the given library will be used.
        No modifications to environment's global seed settings
        are done by this argument.

    Returns
    =======

    sample: float/list/numpy.ndarray
        one sample or a collection of samples of the random expression.

        - sample(X) returns float/numpy.float64/numpy.int64 object.
        - sample(X, size=int/tuple) returns numpy.ndarray object.

    Examples
    ========

    >>> from sympy.stats import Die, sample, Normal, Geometric
    >>> X, Y, Z = Die('X', 6), Die('Y', 6), Die('Z', 6) # Finite Random Variable
    >>> die_roll = sample(X + Y + Z)
    >>> die_roll # doctest: +SKIP
    3
    >>> N = Normal('N', 3, 4) # Continuous Random Variable
    >>> samp = sample(N)
    >>> samp in N.pspace.domain.set
    True
    >>> samp = sample(N, N>0)
    >>> samp > 0
    True
    >>> samp_list = sample(N, size=4)
    >>> [sam in N.pspace.domain.set for sam in samp_list]
    [True, True, True, True]
    >>> sample(N, size = (2,3)) # doctest: +SKIP
    array([[5.42519758, 6.40207856, 4.94991743],
       [1.85819627, 6.83403519, 1.9412172 ]])
    >>> G = Geometric('G', 0.5) # Discrete Random Variable
    >>> samp_list = sample(G, size=3)
    >>> samp_list # doctest: +SKIP
    [1, 3, 2]
    >>> [sam in G.pspace.domain.set for sam in samp_list]
    [True, True, True]
    >>> MN = Normal("MN", [3, 4], [[2, 1], [1, 2]]) # Joint Random Variable
    >>> samp_list = sample(MN, size=4)
    >>> samp_list # doctest: +SKIP
    [array([2.85768055, 3.38954165]),
     array([4.11163337, 4.3176591 ]),
     array([0.79115232, 1.63232916]),
     array([4.01747268, 3.96716083])]
    >>> [tuple(sam) in MN.pspace.domain.set for sam in samp_list]
    [True, True, True, True]

    .. versionchanged:: 1.7.0
        sample used to return an iterator containing the samples instead of value.

    .. versionchanged:: 1.9.0
        sample returns values or array of values instead of an iterator and numsamples is deprecated.

    """

    iterator = sample_iter(expr, condition, size=size, library=library,
                                                        numsamples=numsamples, seed=seed)

    if numsamples != 1:
        sympy_deprecation_warning(
            f"""
            The numsamples parameter to sympy.stats.sample() is deprecated.
            Either use a list comprehension, like

            [sample(...) for i in range({numsamples})]

            or add a dimension to size, like

            sample(..., size={(numsamples,) + size})
            """,
            deprecated_since_version="1.9",
            active_deprecations_target="deprecated-sympy-stats-numsamples",
        )
        return [next(iterator) for i in range(numsamples)]

    return next(iterator)


def sample(iterable, k, weights=None, *, counts=None, strict=False):
    """Return a *k*-length list of elements chosen (without replacement)
    from the *iterable*.

    Similar to :func:`random.sample`, but works on inputs that aren't
    indexable (such as sets and dictionaries) and on inputs where the
    size isn't known in advance (such as generators).

    >>> iterable = range(100)
    >>> sample(iterable, 5)  # doctest: +SKIP
    [81, 60, 96, 16, 4]

    For iterables with repeated elements, you may supply *counts* to
    indicate the repeats.

    >>> iterable = ['a', 'b']
    >>> counts = [3, 4]  # Equivalent to 'a', 'a', 'a', 'b', 'b', 'b', 'b'
    >>> sample(iterable, k=3, counts=counts)  # doctest: +SKIP
    ['a', 'a', 'b']

    An iterable with *weights* may be given:

    >>> iterable = range(100)
    >>> weights = (i * i + 1 for i in range(100))
    >>> sampled = sample(iterable, 5, weights=weights)  # doctest: +SKIP
    [79, 67, 74, 66, 78]

    Weighted selections are made without replacement.
    After an element is selected, it is removed from the pool and the
    relative weights of the other elements increase (this
    does not match the behavior of :func:`random.sample`'s *counts*
    parameter). Note that *weights* may not be used with *counts*.

    If the length of *iterable* is less than *k*,
    ``ValueError`` is raised if *strict* is ``True`` and
    all elements are returned (in shuffled order) if *strict* is ``False``.

    By default, the `Algorithm L <https://w.wiki/ANrM>`__ reservoir sampling
    technique is used. When *weights* are provided,
    `Algorithm A-ExpJ <https://w.wiki/ANrS>`__ is used instead.

    Notes on reproducibility:

    * The algorithms rely on inexact floating-point functions provided
      by the underlying math library (e.g. ``log``, ``log1p``, and ``pow``).
      Those functions can `produce slightly different results
      <https://members.loria.fr/PZimmermann/papers/accuracy.pdf>`_ on
      different builds.  Accordingly, selections can vary across builds
      even for the same seed.

    * The algorithms loop over the input and make selections based on
      ordinal position, so selections from unordered collections (such as
      sets) won't reproduce across sessions on the same platform using the
      same seed.  For example, this won't reproduce::

          >> seed(8675309)
          >> sample(set('abcdefghijklmnopqrstuvwxyz'), 10)
          ['c', 'p', 'e', 'w', 's', 'a', 'j', 'd', 'n', 't']

    """
    iterator = iter(iterable)

    if k < 0:
        raise ValueError('k must be non-negative')

    if k == 0:
        return []

    if weights is not None and counts is not None:
        raise TypeError('weights and counts are mutually exclusive')

    elif weights is not None:
        weights = iter(weights)
        return _sample_weighted(iterator, k, weights, strict)

    elif counts is not None:
        counts = iter(counts)
        return _sample_counted(iterator, k, counts, strict)

    else:
        return _sample_unweighted(iterator, k, strict)


def sample(
    obj_len: int,
    size: int,
    replace: bool,
    weights: np.ndarray | None,
    random_state: np.random.RandomState | np.random.Generator,
) -> np.ndarray:
    """
    Randomly sample `size` indices in `np.arange(obj_len)`.

    Parameters
    ----------
    obj_len : int
        The length of the indices being considered
    size : int
        The number of values to choose
    replace : bool
        Allow or disallow sampling of the same row more than once.
    weights : np.ndarray[np.float64] or None
        If None, equal probability weighting, otherwise weights according
        to the vector normalized
    random_state: np.random.RandomState or np.random.Generator
        State used for the random sampling

    Returns
    -------
    np.ndarray[np.intp]
    """
    if weights is not None:
        weight_sum = weights.sum()
        if weight_sum != 0:
            weights = weights / weight_sum
        else:
            raise ValueError("Invalid weights: weights sum to zero")

        assert weights is not None  # for mypy
        if not replace and size * weights.max() > 1:
            raise ValueError(
                "Weighted sampling cannot be achieved with replace=False. Either "
                "set replace=True or use smaller weights. See the docstring of "
                "sample for details."
            )

    return random_state.choice(obj_len, size=size, replace=replace, p=weights).astype(
        np.intp, copy=False
    )


def sample(
    rng: chex.PRNGKey, state: ReplayBufferState, num_samples: int
) -> Experience:
  """Returns `num_samples` uniformly sampled from the buffer.

  Args:
    rng: `chex.PRNGKey`, a random state
    state: `ReplayBufferState`, a buffer state
    num_samples: `int`, number of samples to draw.

  Returns:
    An iterable over `num_samples` random elements of the buffer.
  Raises:
    AssertionError: If there are less than `num_samples` elements in the buffer
  """

  # When full, the max time index is max_length_time_axis otherwise it is
  # current index.
  max_size = jnp.where(state.is_full, state.capacity, state.entry_index)
  indices = jax.random.randint(
      rng, shape=(num_samples,), minval=0, maxval=max_size
  )
  return jax.tree.map(lambda x: x[indices], state.experience)

