
def flatnonzero(a: ArrayLike):
    return torch.flatten(a).nonzero(as_tuple=True)[0]


def flatnonzero(a):
    """
    Return indices that are non-zero in the flattened version of a.

    This is equivalent to ``np.nonzero(np.ravel(a))[0]``.

    Parameters
    ----------
    a : array_like
        Input data.

    Returns
    -------
    res : ndarray
        Output array, containing the indices of the elements of ``a.ravel()``
        that are non-zero.

    See Also
    --------
    nonzero : Return the indices of the non-zero elements of the input array.
    ravel : Return a 1-D array containing the elements of the input array.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(-2, 3)
    >>> x
    array([-2, -1,  0,  1,  2])
    >>> np.flatnonzero(x)
    array([0, 1, 3, 4])

    Use the indices of the non-zero elements as an index array to extract
    these elements:

    >>> x.ravel()[np.flatnonzero(x)]
    array([-2, -1,  1,  2])

    """
    return np.nonzero(np.ravel(a))[0]


def flatnonzero(a: ArrayLike, *, size: int | None = None,
                fill_value: None | ArrayLike | tuple[ArrayLike, ...] = None) -> Array:
  """Return indices of nonzero elements in a flattened array

  JAX implementation of :func:`numpy.flatnonzero`.

  ``jnp.flatnonzero(x)`` is equivalent to ``nonzero(ravel(a))[0]``. For a full
  discussion of the parameters to this function, refer to :func:`jax.numpy.nonzero`.

  Args:
    a: N-dimensional array.
    size: optional static integer specifying the number of nonzero entries to
      return. See :func:`jax.numpy.nonzero` for more discussion of this parameter.
    fill_value: optional padding value when ``size`` is specified. Defaults to 0.
      See :func:`jax.numpy.nonzero` for more discussion of this parameter.

  Returns:
    Array containing the indices of each nonzero value in the flattened array.

  See Also:
    - :func:`jax.numpy.nonzero`
    - :func:`jax.numpy.where`

  Examples:
    >>> x = jnp.array([[0, 5, 0],
    ...                [6, 0, 8]])
    >>> jnp.flatnonzero(x)
    Array([1, 3, 5], dtype=int32)

    This is equivalent to calling :func:`~jax.numpy.nonzero` on the flattened
    array, and extracting the first entry in the resulting tuple:

    >>> jnp.nonzero(x.ravel())[0]
    Array([1, 3, 5], dtype=int32)

    The returned indices can be used to extract nonzero entries from the
    flattened array:

    >>> indices = jnp.flatnonzero(x)
    >>> x.ravel()[indices]
    Array([5, 6, 8], dtype=int32)
  """
  return nonzero(ravel(a), size=size, fill_value=fill_value)[0]

