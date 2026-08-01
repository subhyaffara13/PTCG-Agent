
def apply_over_axes(func, a, axes):
    """
    Apply a function repeatedly over multiple axes.

    `func` is called as `res = func(a, axis)`, where `axis` is the first
    element of `axes`.  The result `res` of the function call must have
    either the same dimensions as `a` or one less dimension.  If `res`
    has one less dimension than `a`, a dimension is inserted before
    `axis`.  The call to `func` is then repeated for each axis in `axes`,
    with `res` as the first argument.

    Parameters
    ----------
    func : function
        This function must take two arguments, `func(a, axis)`.
    a : array_like
        Input array.
    axes : array_like
        Axes over which `func` is applied; the elements must be integers.

    Returns
    -------
    apply_over_axis : ndarray
        The output array.  The number of dimensions is the same as `a`,
        but the shape can be different.  This depends on whether `func`
        changes the shape of its output with respect to its input.

    See Also
    --------
    apply_along_axis :
        Apply a function to 1-D slices of an array along the given axis.

    Notes
    -----
    This function is equivalent to tuple axis arguments to reorderable ufuncs
    with keepdims=True. Tuple axis arguments to ufuncs have been available since
    version 1.7.0.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(24).reshape(2,3,4)
    >>> a
    array([[[ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11]],
           [[12, 13, 14, 15],
            [16, 17, 18, 19],
            [20, 21, 22, 23]]])

    Sum over axes 0 and 2. The result has same number of dimensions
    as the original array:

    >>> np.apply_over_axes(np.sum, a, [0,2])
    array([[[ 60],
            [ 92],
            [124]]])

    Tuple axis arguments to ufuncs are equivalent:

    >>> np.sum(a, axis=(0,2), keepdims=True)
    array([[[ 60],
            [ 92],
            [124]]])

    """
    val = asarray(a)
    N = a.ndim
    if array(axes).ndim == 0:
        axes = (axes,)
    for axis in axes:
        if axis < 0:
            axis = N + axis
        args = (val, axis)
        res = func(*args)
        if res.ndim == val.ndim:
            val = res
        else:
            res = expand_dims(res, axis)
            if res.ndim == val.ndim:
                val = res
            else:
                raise ValueError("function is not returning "
                                 "an array of the correct shape")
    return val


def apply_over_axes(func, a, axes):
    """
    (This docstring will be overwritten)
    """
    val = asarray(a)
    N = a.ndim
    if array(axes).ndim == 0:
        axes = (axes,)
    for axis in axes:
        if axis < 0:
            axis = N + axis
        args = (val, axis)
        res = func(*args)
        if res.ndim == val.ndim:
            val = res
        else:
            res = ma.expand_dims(res, axis)
            if res.ndim == val.ndim:
                val = res
            else:
                raise ValueError("function is not returning "
                        "an array of the correct shape")
    return val


def apply_over_axes(func: Callable[[ArrayLike, int], Array], a: ArrayLike,
                    axes: Sequence[int]) -> Array:
  """Apply a function repeatedly over specified axes.

  JAX implementation of :func:`numpy.apply_over_axes`.

  Args:
    func: the function to apply, with signature ``func(Array, int) -> Array``, and
      where ``y = func(x, axis)`` must satisfy ``y.ndim in [x.ndim, x.ndim - 1]``.
    a: N-dimensional array over which to apply the function.
    axes: the sequence of axes over which to apply the function.

  Returns:
    An N-dimensional array containing the result of the repeated function application.

  See also:
    - :func:`jax.numpy.apply_along_axis`: apply a 1D function along a single axis.

  Examples:
    This function is designed to have similar semantics to typical associative
    :mod:`jax.numpy` reductions over one or more axes with ``keepdims=True``.
    For example:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])

    >>> jnp.apply_over_axes(jnp.sum, x, [0])
    Array([[5, 7, 9]], dtype=int32)
    >>> jnp.sum(x, [0], keepdims=True)
    Array([[5, 7, 9]], dtype=int32)

    >>> jnp.apply_over_axes(jnp.min, x, [1])
    Array([[1],
           [4]], dtype=int32)
    >>> jnp.min(x, [1], keepdims=True)
    Array([[1],
           [4]], dtype=int32)

    >>> jnp.apply_over_axes(jnp.prod, x, [0, 1])
    Array([[720]], dtype=int32)
    >>> jnp.prod(x, [0, 1], keepdims=True)
    Array([[720]], dtype=int32)
  """
  a_arr = util.ensure_arraylike("apply_over_axes", a)
  for axis in axes:
    b = func(a_arr, axis)
    if b.ndim == a_arr.ndim:
      a_arr = b
    elif b.ndim == a_arr.ndim - 1:
      a_arr = expand_dims(b, axis)
    else:
      raise ValueError("function is not returning an array of the correct shape")
  return a_arr

