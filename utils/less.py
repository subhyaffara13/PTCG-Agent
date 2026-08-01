
def less(x1, x2):
    """
    Return (x1 < x2) element-wise.

    Unlike `numpy.greater`, this comparison is performed by first
    stripping whitespace characters from the end of the string.  This
    behavior is provided for backward-compatibility with numarray.

    Parameters
    ----------
    x1, x2 : array_like of str or unicode
        Input arrays of the same shape.

    Returns
    -------
    out : ndarray
        Output array of bools.

    See Also
    --------
    equal, not_equal, greater_equal, less_equal, greater

    Examples
    --------
    >>> import numpy as np
    >>> x1 = np.array(['a', 'b', 'c'])
    >>> np.char.less(x1, 'b')
    array([True, False, False])

    """
    return compare_chararrays(x1, x2, '<', True)


def less(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise truth value of ``x < y``.

  JAX implementation of :obj:`numpy.less`.

  Args:
    x: input array or scalar.
    y: input array or scalar. ``x`` and ``y`` must either have same shape or be
      broadcast compatible.

  Returns:
    An array containing boolean values. ``True`` if the elements of ``x < y``,
    and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.greater`: Returns element-wise truth value of ``x > y``.
    - :func:`jax.numpy.greater_equal`: Returns element-wise truth value of
      ``x >= y``.
    - :func:`jax.numpy.less_equal`: Returns element-wise truth value of ``x <= y``.

  Examples:
    Scalar inputs:

    >>> jnp.less(3, 7)
    Array(True, dtype=bool, weak_type=True)

    Inputs with same shape:

    >>> x = jnp.array([5, 9, -3])
    >>> y = jnp.array([1, 6, 4])
    >>> jnp.less(x, y)
    Array([False, False,  True], dtype=bool)

    Inputs with broadcast compatibility:

    >>> x1 = jnp.array([[2, -4, 6, -8],
    ...                 [-1, 5, -3, 7]])
    >>> y1 = jnp.array([0, 3, -5, 9])
    >>> jnp.less(x1, y1)
    Array([[False,  True, False,  True],
           [ True, False, False,  True]], dtype=bool)
  """
  return _complex_comparison(lax.lt, *promote_args("less", x, y))

