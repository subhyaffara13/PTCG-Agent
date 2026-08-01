
def mask_indices(n, mask_func, k=0):
    """
    Return the indices to access (n, n) arrays, given a masking function.

    Assume `mask_func` is a function that, for a square array a of size
    ``(n, n)`` with a possible offset argument `k`, when called as
    ``mask_func(a, k)`` returns a new array with zeros in certain locations
    (functions like `triu` or `tril` do precisely this). Then this function
    returns the indices where the non-zero values would be located.

    Parameters
    ----------
    n : int
        The returned indices will be valid to access arrays of shape (n, n).
    mask_func : callable
        A function whose call signature is similar to that of `triu`, `tril`.
        That is, ``mask_func(x, k)`` returns a boolean array, shaped like `x`.
        `k` is an optional argument to the function.
    k : scalar
        An optional argument which is passed through to `mask_func`. Functions
        like `triu`, `tril` take a second argument that is interpreted as an
        offset.

    Returns
    -------
    indices : tuple of arrays.
        The `n` arrays of indices corresponding to the locations where
        ``mask_func(np.ones((n, n)), k)`` is True.

    See Also
    --------
    triu, tril, triu_indices, tril_indices

    Examples
    --------
    >>> import numpy as np

    These are the indices that would allow you to access the upper triangular
    part of any 3x3 array:

    >>> iu = np.mask_indices(3, np.triu)

    For example, if `a` is a 3x3 array:

    >>> a = np.arange(9).reshape(3, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])
    >>> a[iu]
    array([0, 1, 2, 4, 5, 8])

    An offset can be passed also to the masking function.  This gets us the
    indices starting on the first diagonal right of the main one:

    >>> iu1 = np.mask_indices(3, np.triu, 1)

    with which we now extract only three elements:

    >>> a[iu1]
    array([1, 2, 5])

    """
    m = ones((n, n), int)
    a = mask_func(m, k)
    return nonzero(a != 0)


def mask_indices(n: int,
                 mask_func: Callable[[ArrayLike, int], Array],
                 k: int = 0, *, size: int | None = None) -> tuple[Array, Array]:
  """Return indices of a mask of an (n, n) array.

  Args:
    n: static integer array dimension.
    mask_func: a function that takes a shape ``(n, n)`` array and
      an optional offset ``k``, and returns a shape ``(n, n)`` mask.
      Examples of functions with this signature are
      :func:`~jax.numpy.triu` and :func:`~jax.numpy.tril`.
    k: a scalar value passed to ``mask_func``.
    size: optional argument specifying the static size of the output arrays.
      This is passed to :func:`~jax.numpy.nonzero` when generating the indices
      from the mask.

  Returns:
    a tuple of indices where ``mask_func`` is nonzero.

  See also:
    - :func:`jax.numpy.triu_indices`: compute ``mask_indices`` for :func:`~jax.numpy.triu`.
    - :func:`jax.numpy.tril_indices`: compute ``mask_indices`` for :func:`~jax.numpy.tril`.

  Examples:
    Calling ``mask_indices`` on built-in masking functions:

    >>> jnp.mask_indices(3, jnp.triu)
    (Array([0, 0, 0, 1, 1, 2], dtype=int32), Array([0, 1, 2, 1, 2, 2], dtype=int32))

    >>> jnp.mask_indices(3, jnp.tril)
    (Array([0, 1, 1, 2, 2, 2], dtype=int32), Array([0, 0, 1, 0, 1, 2], dtype=int32))

    Calling ``mask_indices`` on a custom masking function:

    >>> def mask_func(x, k=0):
    ...   i = jnp.arange(x.shape[0])[:, None]
    ...   j = jnp.arange(x.shape[1])
    ...   return (i + 1) % (j + 1 + k) == 0
    >>> mask_func(jnp.ones((3, 3)))
    Array([[ True, False, False],
           [ True,  True, False],
           [ True, False,  True]], dtype=bool)
    >>> jnp.mask_indices(3, mask_func)
    (Array([0, 1, 1, 2, 2], dtype=int32), Array([0, 0, 1, 0, 2], dtype=int32))
  """
  i, j = nonzero(mask_func(array_creation.ones((n, n)), k), size=size)
  return (i, j)

