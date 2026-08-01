
def not_equal(x1, x2):
    """
    Return (x1 != x2) element-wise.

    Unlike `numpy.not_equal`, this comparison is performed by first
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
    equal, greater_equal, less_equal, greater, less

    Examples
    --------
    >>> import numpy as np
    >>> x1 = np.array(['a', 'b', 'c'])
    >>> np.char.not_equal(x1, 'b')
    array([ True, False,  True])

    """
    return compare_chararrays(x1, x2, '!=', True)


def not_equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Returns element-wise truth value of ``x != y``.

  JAX implementation of :obj:`numpy.not_equal`. This function provides the
  implementation of the ``!=`` operator for JAX arrays.

  Args:
    x: input array or scalar.
    y: input array or scalar. ``x`` and ``y`` should either have same shape or be
      broadcast compatible.

  Returns:
    A boolean array containing ``True`` where the elements of ``x != y`` and
    ``False`` otherwise.

  See also:
    - :func:`jax.numpy.equal`: Returns element-wise truth value of ``x == y``.
    - :func:`jax.numpy.greater_equal`: Returns element-wise truth value of
      ``x >= y``.
    - :func:`jax.numpy.less_equal`: Returns element-wise truth value of ``x <= y``.
    - :func:`jax.numpy.greater`: Returns element-wise truth value of ``x > y``.
    - :func:`jax.numpy.less`: Returns element-wise truth value of ``x < y``.

  Examples:
    >>> jnp.not_equal(0., -0.)
    Array(False, dtype=bool, weak_type=True)
    >>> jnp.not_equal(-2, 2)
    Array(True, dtype=bool, weak_type=True)
    >>> jnp.not_equal(1, 1.)
    Array(False, dtype=bool, weak_type=True)
    >>> jnp.not_equal(5, jnp.array(5))
    Array(False, dtype=bool, weak_type=True)
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> y = jnp.array([1, 5, 9])
    >>> jnp.not_equal(x, y)
    Array([[False,  True,  True],
           [ True, False,  True],
           [ True,  True, False]], dtype=bool)
    >>> x != y
    Array([[False,  True,  True],
           [ True, False,  True],
           [ True,  True, False]], dtype=bool)
  """
  return lax.ne(*promote_args("not_equal", x, y))

