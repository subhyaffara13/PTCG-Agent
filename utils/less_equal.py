
def less_equal(x1, x2):
    """
    Return (x1 <= x2) element-wise.

    Unlike `numpy.less_equal`, this comparison is performed by first
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
    equal, not_equal, greater_equal, greater, less

    Examples
    --------
    >>> import numpy as np
    >>> x1 = np.array(['a', 'b', 'c'])
    >>> np.char.less_equal(x1, 'b')
    array([ True,  True, False])

    """
    return compare_chararrays(x1, x2, '<=', True)


def less_equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise truth value of ``x <= y``.

  JAX implementation of :obj:`numpy.less_equal`.

  Args:
    x: input array or scalar.
    y: input array or scalar. ``x`` and ``y`` must have either same shape or be
      broadcast compatible.

  Returns:
    An array containing the boolean values. ``True`` if the elements of ``x <= y``,
    and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.greater_equal`: Returns element-wise truth value of
      ``x >= y``.
    - :func:`jax.numpy.greater`: Returns element-wise truth value of ``x > y``.
    - :func:`jax.numpy.less`: Returns element-wise truth value of ``x < y``.

  Examples:
    Scalar inputs:

    >>> jnp.less_equal(6, -2)
    Array(False, dtype=bool, weak_type=True)

    Inputs with same shape:

    >>> x = jnp.array([-4, 1, 7])
    >>> y = jnp.array([2, -3, 8])
    >>> jnp.less_equal(x, y)
    Array([ True, False,  True], dtype=bool)

    Inputs with broadcast compatibility:

    >>> x1 = jnp.array([2, -5, 9])
    >>> y1 = jnp.array([[1, -6, 5],
    ...                 [-2, 4, -6]])
    >>> jnp.less_equal(x1, y1)
    Array([[False, False, False],
           [False,  True, False]], dtype=bool)
  """
  return _complex_comparison(lax.le, *promote_args("less_equal", x, y))

