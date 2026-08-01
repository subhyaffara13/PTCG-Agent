
def rollaxis(a: ArrayLike, axis, start=0):
    # Straight vendor from:
    # https://github.com/numpy/numpy/blob/v1.24.0/numpy/core/numeric.py#L1259
    #
    # Also note this function in NumPy is mostly retained for backwards compat
    # (https://stackoverflow.com/questions/29891583/reason-why-numpy-rollaxis-is-so-confusing)
    # so let's not touch it unless hard pressed.
    n = a.ndim
    axis = _util.normalize_axis_index(axis, n)
    if start < 0:
        start += n
    msg = "'%s' arg requires %d <= %s < %d, but %d was passed in"
    if not (0 <= start < n + 1):
        raise _util.AxisError(msg % ("start", -n, "start", n + 1, start))
    if axis < start:
        # it's been removed
        start -= 1
    if axis == start:
        # numpy returns a view, here we try returning the tensor itself
        # return tensor[...]
        return a
    axes = list(range(n))
    axes.remove(axis)
    axes.insert(start, axis)
    return a.view(axes)


def rollaxis(a, axis, start=0):
    """
    Roll the specified axis backwards, until it lies in a given position.

    This function continues to be supported for backward compatibility, but you
    should prefer `moveaxis`. The `moveaxis` function was added in NumPy
    1.11.

    Parameters
    ----------
    a : ndarray
        Input array.
    axis : int
        The axis to be rolled. The positions of the other axes do not
        change relative to one another.
    start : int, optional
        When ``start <= axis``, the axis is rolled back until it lies in
        this position. When ``start > axis``, the axis is rolled until it
        lies before this position. The default, 0, results in a "complete"
        roll. The following table describes how negative values of ``start``
        are interpreted:

        .. table::
           :align: left

           +-------------------+----------------------+
           |     ``start``     | Normalized ``start`` |
           +===================+======================+
           | ``-(arr.ndim+1)`` | raise ``AxisError``  |
           +-------------------+----------------------+
           | ``-arr.ndim``     | 0                    |
           +-------------------+----------------------+
           | |vdots|           | |vdots|              |
           +-------------------+----------------------+
           | ``-1``            | ``arr.ndim-1``       |
           +-------------------+----------------------+
           | ``0``             | ``0``                |
           +-------------------+----------------------+
           | |vdots|           | |vdots|              |
           +-------------------+----------------------+
           | ``arr.ndim``      | ``arr.ndim``         |
           +-------------------+----------------------+
           | ``arr.ndim + 1``  | raise ``AxisError``  |
           +-------------------+----------------------+

        .. |vdots|   unicode:: U+22EE .. Vertical Ellipsis

    Returns
    -------
    res : ndarray
        For NumPy >= 1.10.0 a view of `a` is always returned. For earlier
        NumPy versions a view of `a` is returned only if the order of the
        axes is changed, otherwise the input array is returned.

    See Also
    --------
    moveaxis : Move array axes to new positions.
    roll : Roll the elements of an array by a number of positions along a
        given axis.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ones((3,4,5,6))
    >>> np.rollaxis(a, 3, 1).shape
    (3, 6, 4, 5)
    >>> np.rollaxis(a, 2).shape
    (5, 3, 4, 6)
    >>> np.rollaxis(a, 1, 4).shape
    (3, 5, 6, 4)

    """
    n = a.ndim
    axis = normalize_axis_index(axis, n)
    if start < 0:
        start += n
    msg = "'%s' arg requires %d <= %s < %d, but %d was passed in"
    if not (0 <= start < n + 1):
        raise AxisError(msg % ('start', -n, 'start', n + 1, start))
    if axis < start:
        # it's been removed
        start -= 1
    if axis == start:
        return a[...]
    axes = list(range(n))
    axes.remove(axis)
    axes.insert(start, axis)
    return a.transpose(axes)


def rollaxis(a: ArrayLike, axis: int, start: int = 0) -> Array:
  """Roll the specified axis to a given position.

  JAX implementation of :func:`numpy.rollaxis`.

  This function exists for compatibility with NumPy, but in most cases the newer
  :func:`jax.numpy.moveaxis` instead, because the meaning of its arguments is
  more intuitive.

  Args:
    a: input array.
    axis: index of the axis to roll forward.
    start: index toward which the axis will be rolled (default = 0). After
      normalizing negative axes, if ``start <= axis``, the axis is rolled to
      the ``start`` index; if ``start > axis``, the axis is rolled until the
      position before ``start``.

  Returns:
    Copy of ``a`` with rolled axis.

  Notes:
    Unlike :func:`numpy.rollaxis`, :func:`jax.numpy.rollaxis` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize away
    such copies when possible, so this doesn't have performance impacts in practice.

  See also:
    - :func:`jax.numpy.moveaxis`: newer API with clearer semantics than ``rollaxis``;
      this should be preferred to ``rollaxis`` in most cases.
    - :func:`jax.numpy.swapaxes`: swap two axes.
    - :func:`jax.numpy.transpose`: general permutation of axes.

  Examples:
    >>> a = jnp.ones((2, 3, 4, 5))

    Roll axis 2 to the start of the array:

    >>> jnp.rollaxis(a, 2).shape
    (4, 2, 3, 5)

    Roll axis 1 to the end of the array:

    >>> jnp.rollaxis(a, 1, a.ndim).shape
    (2, 4, 5, 3)

    Equivalent of these two with :func:`~jax.numpy.moveaxis`

    >>> jnp.moveaxis(a, 2, 0).shape
    (4, 2, 3, 5)
    >>> jnp.moveaxis(a, 1, -1).shape
    (2, 4, 5, 3)
  """
  a = util.ensure_arraylike("rollaxis", a)
  start = core.concrete_or_error(operator.index, start, "'start' argument of jnp.rollaxis()")
  a_ndim = np.ndim(a)
  axis = _canonicalize_axis(axis, a_ndim)
  if not (-a_ndim <= start <= a_ndim):
    raise ValueError(f"{start=} must satisfy {-a_ndim}<=start<={a_ndim}")
  if start < 0:
    start += a_ndim
  if start > axis:
    start -= 1
  return moveaxis(a, axis, start)

