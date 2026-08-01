
def greater(x1, x2):
    """
    Return (x1 > x2) element-wise.

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
    equal, not_equal, greater_equal, less_equal, less

    Examples
    --------
    >>> import numpy as np
    >>> x1 = np.array(['a', 'b', 'c'])
    >>> np.char.greater(x1, 'b')
    array([False, False,  True])

    """
    return compare_chararrays(x1, x2, '>', True)


def greater(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise truth value of ``x > y``.

  JAX implementation of :obj:`numpy.greater`.

  Args:
    x: input array or scalar.
    y: input array or scalar. ``x`` and ``y`` must either have same shape or be
      broadcast compatible.

  Returns:
    An array containing boolean values. ``True`` if the elements of ``x > y``,
    and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.less`: Returns element-wise truth value of ``x < y``.
    - :func:`jax.numpy.greater_equal`: Returns element-wise truth value of
      ``x >= y``.
    - :func:`jax.numpy.less_equal`: Returns element-wise truth value of ``x <= y``.

  Examples:
    Scalar inputs:

    >>> jnp.greater(5, 2)
    Array(True, dtype=bool, weak_type=True)

    Inputs with same shape:

    >>> x = jnp.array([5, 9, -2])
    >>> y = jnp.array([4, -1, 6])
    >>> jnp.greater(x, y)
    Array([ True,  True, False], dtype=bool)

    Inputs with broadcast compatibility:

    >>> x1 = jnp.array([[5, -6, 7],
    ...                 [-2, 5, 9]])
    >>> y1 = jnp.array([-4, 3, 10])
    >>> jnp.greater(x1, y1)
    Array([[ True, False, False],
           [ True,  True, False]], dtype=bool)
  """
  return _complex_comparison(lax.gt, *promote_args("greater", x, y))

