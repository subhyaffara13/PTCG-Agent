
def equal(one, two):
    """
    Check if two things are equal evading some Python type hierarchy semantics.

    Specifically in JSON Schema, evade `bool` inheriting from `int`,
    recursing into sequences to do the same.
    """
    if one is two:
        return True
    if isinstance(one, str) or isinstance(two, str):
        return one == two
    if isinstance(one, Sequence) and isinstance(two, Sequence):
        return _sequence_equal(one, two)
    if isinstance(one, Mapping) and isinstance(two, Mapping):
        return _mapping_equal(one, two)
    return unbool(one) == unbool(two)


def equal(a: TensorLikeType, b: TensorLikeType) -> bool:
    utils.check_same_device(a, b, allow_cpu_scalar_tensors=False)
    utils.check_same_dtype(a, b)

    # Shape check
    if a.ndim != b.ndim:
        return False

    for x, y in zip(a.shape, b.shape):
        if x != y:
            return False

    # Short-circuits if there are no elements to validate
    if a.numel() == 0:
        return True

    return item(all(eq(a, b)))  # type: ignore[return-value]


def equal(types, args, kwargs, process_group):
    return binary_cmp(torch.equal, types, args, kwargs, process_group)


def equal(n):
    """
    Match a numeric value
    """
    return between(n, n)


def equal(x1, x2):
    """
    Return (x1 == x2) element-wise.

    Unlike `numpy.equal`, this comparison is performed by first
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

    Examples
    --------
    >>> import numpy as np
    >>> y = "aa "
    >>> x = "aa"
    >>> np.char.equal(x, y)
    array(True)

    See Also
    --------
    not_equal, greater_equal, less_equal, greater, less
    """
    return compare_chararrays(x1, x2, '==', True)


def equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Returns element-wise truth value of ``x == y``.

  JAX implementation of :obj:`numpy.equal`. This function provides the implementation
  of the ``==`` operator for JAX arrays.

  Args:
    x: input array or scalar.
    y: input array or scalar. ``x`` and ``y`` should either have same shape or be
      broadcast compatible.

  Returns:
    A boolean array containing ``True`` where the elements of ``x == y`` and
    ``False`` otherwise.

  See also:
    - :func:`jax.numpy.not_equal`: Returns element-wise truth value of ``x != y``.
    - :func:`jax.numpy.greater_equal`: Returns element-wise truth value of
      ``x >= y``.
    - :func:`jax.numpy.less_equal`: Returns element-wise truth value of ``x <= y``.
    - :func:`jax.numpy.greater`: Returns element-wise truth value of ``x > y``.
    - :func:`jax.numpy.less`: Returns element-wise truth value of ``x < y``.

  Examples:
    >>> jnp.equal(0., -0.)
    Array(True, dtype=bool, weak_type=True)
    >>> jnp.equal(1, 1.)
    Array(True, dtype=bool, weak_type=True)
    >>> jnp.equal(5, jnp.array(5))
    Array(True, dtype=bool, weak_type=True)
    >>> jnp.equal(2, -2)
    Array(False, dtype=bool, weak_type=True)
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> y = jnp.array([1, 5, 9])
    >>> jnp.equal(x, y)
    Array([[ True, False, False],
           [False,  True, False],
           [False, False,  True]], dtype=bool)
    >>> x == y
    Array([[ True, False, False],
           [False,  True, False],
           [False, False,  True]], dtype=bool)
  """
  return lax.eq(*promote_args("equal", x, y))


def equal(lst):
    lst = list(lst)
    t = iter(lst)
    first = next(t)
    assert all(item == first for item in t), "Expected all items to be equal: %s" % lst
    return first

