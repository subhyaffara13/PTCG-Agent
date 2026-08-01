
def greater_equal(x1, x2):
    """
    Return (x1 >= x2) element-wise.

    Unlike `numpy.greater_equal`, this comparison is performed by
    first stripping whitespace characters from the end of the string.
    This behavior is provided for backward-compatibility with
    numarray.

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
    equal, not_equal, less_equal, greater, less

    Examples
    --------
    >>> import numpy as np
    >>> x1 = np.array(['a', 'b', 'c'])
    >>> np.char.greater_equal(x1, 'b')
    array([False,  True,  True])

    """
    return compare_chararrays(x1, x2, '>=', True)


def greater_equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise truth value of ``x >= y``.

  JAX implementation of :obj:`numpy.greater_equal`.

  Args:
    x: input array or scalar.
    y: input array or scalar. ``x`` and ``y`` must either have same shape or be
      broadcast compatible.

  Returns:
    An array containing boolean values. ``True`` if the elements of ``x >= y``,
    and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.less_equal`: Returns element-wise truth value of ``x <= y``.
    - :func:`jax.numpy.greater`: Returns element-wise truth value of ``x > y``.
    - :func:`jax.numpy.less`: Returns element-wise truth value of ``x < y``.

  Examples:
    Scalar inputs:

    >>> jnp.greater_equal(4, 7)
    Array(False, dtype=bool, weak_type=True)

    Inputs with same shape:

    >>> x = jnp.array([2, 5, -1])
    >>> y = jnp.array([-6, 4, 3])
    >>> jnp.greater_equal(x, y)
    Array([ True,  True, False], dtype=bool)

    Inputs with broadcast compatibility:

    >>> x1 = jnp.array([[3, -1, 4],
    ...                 [5, 9, -6]])
    >>> y1 = jnp.array([-1, 4, 2])
    >>> jnp.greater_equal(x1, y1)
    Array([[ True, False,  True],
           [ True,  True, False]], dtype=bool)
  """
  return _complex_comparison(lax.ge, *promote_args("greater_equal", x, y))

