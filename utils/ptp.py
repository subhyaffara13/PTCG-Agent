
def ptp(
    a: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    keepdims: KeepDims = False,
):
    return a.amax(axis) - a.amin(axis)


def ptp(obj, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
    try:
        return obj.ptp(axis, out=out, fill_value=fill_value, **kwargs)
    except (AttributeError, TypeError):
        # If obj doesn't have a ptp method or if the method doesn't accept
        # a fill_value argument
        return asanyarray(obj).ptp(axis=axis, fill_value=fill_value,
                                   out=out, **kwargs)


def ptp(a, axis=None, out=None, keepdims=np._NoValue):
    """
    Range of values (maximum - minimum) along an axis.

    The name of the function comes from the acronym for 'peak to peak'.

    .. warning::
        `ptp` preserves the data type of the array. This means the
        return value for an input of signed integers with n bits
        (e.g. `numpy.int8`, `numpy.int16`, etc) is also a signed integer
        with n bits.  In that case, peak-to-peak values greater than
        ``2**(n-1)-1`` will be returned as negative values. An example
        with a work-around is shown below.

    Parameters
    ----------
    a : array_like
        Input values.
    axis : None or int or tuple of ints, optional
        Axis along which to find the peaks.  By default, flatten the
        array.  `axis` may be negative, in
        which case it counts from the last to the first axis.
        If this is a tuple of ints, a reduction is performed on multiple
        axes, instead of a single axis or all the axes as before.
    out : array_like
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output,
        but the type of the output values will be cast if necessary.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `ptp` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.

    Returns
    -------
    ptp : ndarray or scalar
        The range of a given array - `scalar` if array is one-dimensional
        or a new array holding the result along the given axis

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([[4, 9, 2, 10],
    ...               [6, 9, 7, 12]])

    >>> np.ptp(x, axis=1)
    array([8, 6])

    >>> np.ptp(x, axis=0)
    array([2, 0, 5, 2])

    >>> np.ptp(x)
    10

    This example shows that a negative value can be returned when
    the input is an array of signed integers.

    >>> y = np.array([[1, 127],
    ...               [0, 127],
    ...               [-1, 127],
    ...               [-2, 127]], dtype=np.int8)
    >>> np.ptp(y, axis=1)
    array([ 126,  127, -128, -127], dtype=int8)

    A work-around is to use the `view()` method to view the result as
    unsigned integers with the same bit width:

    >>> np.ptp(y, axis=1).view(np.uint8)
    array([126, 127, 128, 129], dtype=uint8)

    """
    kwargs = {}
    if keepdims is not np._NoValue:
        kwargs['keepdims'] = keepdims
    return _methods._ptp(a, axis=axis, out=out, **kwargs)


def ptp(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False) -> Array:
  r"""Return the peak-to-peak range along a given axis.

  JAX implementation of :func:`numpy.ptp`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      range is computed. If None, the range is computed on the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    out: Unused by JAX.

  Returns:
    An array with the range of elements along specified axis of input.

  Examples:
    By default, ``jnp.ptp`` computes the range along all axes.

    >>> x = jnp.array([[1, 3, 5, 2],
    ...                [4, 6, 8, 1],
    ...                [7, 9, 3, 4]])
    >>> jnp.ptp(x)
    Array(8, dtype=int32)

    If ``axis=1``, computes the range along axis 1.

    >>> jnp.ptp(x, axis=1)
    Array([4, 7, 6], dtype=int32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.ptp(x, axis=1, keepdims=True)
    Array([[4],
           [7],
           [6]], dtype=int32)
  """
  a = ensure_arraylike("ptp", a)
  return _ptp(a, _ensure_optional_axes(axis), out, keepdims)

