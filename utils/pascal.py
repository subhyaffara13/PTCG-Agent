
def pascal(n, kind='symmetric', exact=True):
    """
    Returns the n x n Pascal matrix.

    The Pascal matrix is a matrix containing the binomial coefficients as
    its elements.

    Parameters
    ----------
    n : int
        The size of the matrix to create; that is, the result is an n x n
        matrix.
    kind : str, optional
        Must be one of 'symmetric', 'lower', or 'upper'.
        Default is 'symmetric'.
    exact : bool, optional
        If `exact` is True, the result is either an array of type
        numpy.uint64 (if n < 35) or an object array of Python long integers.
        If `exact` is False, the coefficients in the matrix are computed using
        `scipy.special.comb` with ``exact=False``. The result will be a floating
        point array, and the values in the array will not be the exact
        coefficients, but this version is much faster than ``exact=True``.

    Returns
    -------
    p : (n, n) ndarray
        The Pascal matrix.

    See Also
    --------
    invpascal

    Notes
    -----
    See https://en.wikipedia.org/wiki/Pascal_matrix for more information
    about Pascal matrices.

    .. versionadded:: 0.11.0

    Examples
    --------
    >>> from scipy.linalg import pascal
    >>> pascal(4)
    array([[ 1,  1,  1,  1],
           [ 1,  2,  3,  4],
           [ 1,  3,  6, 10],
           [ 1,  4, 10, 20]], dtype=uint64)
    >>> pascal(4, kind='lower')
    array([[1, 0, 0, 0],
           [1, 1, 0, 0],
           [1, 2, 1, 0],
           [1, 3, 3, 1]], dtype=uint64)
    >>> pascal(50)[-1, -1]
    25477612258980856902730428600
    >>> from scipy.special import comb
    >>> comb(98, 49, exact=True)
    25477612258980856902730428600

    """

    from scipy.special import comb
    if kind not in ['symmetric', 'lower', 'upper']:
        raise ValueError("kind must be 'symmetric', 'lower', or 'upper'")

    if exact:
        if n >= 35:
            L_n = np.empty((n, n), dtype=object)
            L_n.fill(0)
        else:
            L_n = np.zeros((n, n), dtype=np.uint64)
        for i in range(n):
            for j in range(i + 1):
                L_n[i, j] = comb(i, j, exact=True)
    else:
        L_n = comb(*np.ogrid[:n, :n])

    if kind == 'lower':
        p = L_n
    elif kind == 'upper':
        p = L_n.T
    else:
        p = np.dot(L_n, L_n.T)

    return p


def pascal(n: int, kind: str | None = None) -> Array:
  r"""Create a Pascal matrix approximation of order n.

  JAX implementation of :func:`scipy.linalg.pascal`.

  The elements of the Pascal matrix approximate the binomial coefficients. This
  implementation is not exact as JAX does not support exact factorials.

  Args:
    n: the size of the matrix to create.
    kind: (optional) must be one of ``lower``, ``upper``, or ``symmetric`` (default).

  Returns:
    A Pascal matrix of shape ``(n, n)``

  Examples:
    >>> with jnp.printoptions(precision=3):
    ...   print(jax.scipy.linalg.pascal(3, kind="lower"))
    ...   print(jax.scipy.linalg.pascal(4, kind="upper"))
    ...   print(jax.scipy.linalg.pascal(5))
    [[1. 0. 0.]
     [1. 1. 0.]
     [1. 2. 1.]]
    [[1. 1. 1. 1.]
     [0. 1. 2. 3.]
     [0. 0. 1. 3.]
     [0. 0. 0. 1.]]
    [[ 1.  1.  1.  1.  1.]
     [ 1.  2.  3.  4.  5.]
     [ 1.  3.  6. 10. 15.]
     [ 1.  4. 10. 20. 35.]
     [ 1.  5. 15. 35. 70.]]
  """
  if kind is None:
    kind = "symmetric"

  valid_kind = ["symmetric", "lower", "upper"]

  if kind not in valid_kind:
    raise ValueError(f"Expected kind to be on of: {valid_kind}; got {kind}")

  a = jnp.arange(n, dtype=np.float32)

  L_n = _binom(a[:, None], a[None, :])

  if kind == "lower":
    return L_n

  if kind == "upper":
    return L_n.T

  return jnp.dot(L_n, L_n.T)

