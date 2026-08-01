
def leslie(f, s):
    """
    Create a Leslie matrix.

    Given the length n array of fecundity coefficients `f` and the length
    n-1 array of survival coefficients `s`, return the associated Leslie
    matrix.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    f : (N,) array_like
        The "fecundity" coefficients.
    s : (N-1,) array_like
        The "survival" coefficients. The length of `s` must be one less
        than the length of `f`, and it must be at least 1.

    Returns
    -------
    L : (N, N) ndarray
        The array is zero except for the first row,
        which is `f`, and the first sub-diagonal, which is `s`.
        The data-type of the array will be the data-type of
        ``f[0]+s[0]``.

    Notes
    -----
    The Leslie matrix is used to model discrete-time, age-structured
    population growth [1]_ [2]_. In a population with `n` age classes, two sets
    of parameters define a Leslie matrix: the `n` "fecundity coefficients",
    which give the number of offspring per-capita produced by each age
    class, and the `n` - 1 "survival coefficients", which give the
    per-capita survival rate of each age class.

    References
    ----------
    .. [1] P. H. Leslie, On the use of matrices in certain population
           mathematics, Biometrika, Vol. 33, No. 3, 183--212 (Nov. 1945)
    .. [2] P. H. Leslie, Some further notes on the use of matrices in
           population mathematics, Biometrika, Vol. 35, No. 3/4, 213--245
           (Dec. 1948)

    Examples
    --------
    >>> from scipy.linalg import leslie
    >>> leslie([0.1, 2.0, 1.0, 0.1], [0.2, 0.8, 0.7])
    array([[ 0.1,  2. ,  1. ,  0.1],
           [ 0.2,  0. ,  0. ,  0. ],
           [ 0. ,  0.8,  0. ,  0. ],
           [ 0. ,  0. ,  0.7,  0. ]])

    """
    f = np.atleast_1d(f)
    s = np.atleast_1d(s)

    if f.shape[-1] != s.shape[-1] + 1:
        raise ValueError("Incorrect lengths for f and s. The length of s along "
                         "the last axis must be one less than the length of f.")
    if s.shape[-1] == 0:
        raise ValueError("The length of s must be at least 1.")

    n = f.shape[-1]
    tmp = f[0] + s[0]
    a = np.zeros((n, n), dtype=tmp.dtype)
    a[0] = f
    a[list(range(1, n)), list(range(0, n - 1))] = s
    return a


def leslie(f: ArrayLike, s: ArrayLike) -> Array:
  r"""Construct a Leslie matrix.

  JAX implementation of :func:`scipy.linalg.leslie`.

  Given fecundity coefficients ``f`` of shape ``(..., N)`` and survival
  coefficients ``s`` of shape ``(..., N - 1)``, the Leslie matrix has ``f`` as
  its first row, ``s`` along its first sub-diagonal, and zeros elsewhere.

  Args:
    f: array of shape ``(..., N)`` with ``N >= 2`` containing the fecundity
      coefficients.
    s: array of shape ``(..., N - 1)`` containing the survival coefficients.

  Returns:
    A Leslie matrix of shape ``(..., N, N)``.

  Examples:
    >>> jax.scipy.linalg.leslie(jnp.array([0.1, 2.0, 1.0, 0.1]),
    ...                         jnp.array([0.2, 0.8, 0.7]))
    Array([[0.1, 2. , 1. , 0.1],
           [0.2, 0. , 0. , 0. ],
           [0. , 0.8, 0. , 0. ],
           [0. , 0. , 0.7, 0. ]], dtype=float32)
  """
  check_arraylike("leslie", f, s)
  f_arr = jnp.atleast_1d(f)
  s_arr = jnp.atleast_1d(s)
  if f_arr.shape[-1] < 2:
    raise ValueError(
        "The length of f along the last axis must be at least 2; "
        f"got shape {f_arr.shape}.")
  if s_arr.shape[-1] != f_arr.shape[-1] - 1:
    raise ValueError(
        "Incorrect lengths for f and s. The length of s along the last axis "
        f"must be one less than the length of f; got f shape {f_arr.shape} "
        f"and s shape {s_arr.shape}.")
  return _leslie(f_arr, s_arr)

