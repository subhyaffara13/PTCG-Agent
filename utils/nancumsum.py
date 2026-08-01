
def nancumsum(a, axis=None, dtype=None, out=None):
    """
    Return the cumulative sum of array elements over a given axis treating Not a
    Numbers (NaNs) as zero.  The cumulative sum does not change when NaNs are
    encountered and leading NaNs are replaced by zeros.

    Zeros are returned for slices that are all-NaN or empty.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int, optional
        Axis along which the cumulative sum is computed. The default
        (None) is to compute the cumsum over the flattened array.
    dtype : dtype, optional
        Type of the returned array and of the accumulator in which the
        elements are summed.  If `dtype` is not specified, it defaults
        to the dtype of `a`, unless `a` has an integer dtype with a
        precision less than that of the default platform integer.  In
        that case, the default platform integer is used.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output
        but the type will be cast if necessary. See :ref:`ufuncs-output-type` for
        more details.

    Returns
    -------
    nancumsum : ndarray.
        A new array holding the result is returned unless `out` is
        specified, in which it is returned. The result has the same
        size as `a`, and the same shape as `a` if `axis` is not None
        or `a` is a 1-d array.

    See Also
    --------
    numpy.cumsum : Cumulative sum across array propagating NaNs.
    isnan : Show which elements are NaN.

    Examples
    --------
    >>> import numpy as np
    >>> np.nancumsum(1)
    array([1])
    >>> np.nancumsum([1])
    array([1])
    >>> np.nancumsum([1, np.nan])
    array([1.,  1.])
    >>> a = np.array([[1, 2], [3, np.nan]])
    >>> np.nancumsum(a)
    array([1.,  3.,  6.,  6.])
    >>> np.nancumsum(a, axis=0)
    array([[1.,  2.],
           [4.,  2.]])
    >>> np.nancumsum(a, axis=1)
    array([[1.,  3.],
           [3.,  3.]])

    """
    a, mask = _replace_nan(a, 0)
    return np.cumsum(a, axis=axis, dtype=dtype, out=out)


def nancumsum(a: ArrayLike, axis: int | None = None,
              dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative sum of elements along an axis, ignoring NaN values.

  JAX implementation of :func:`numpy.nancumsum`.

  Args:
    a: N-dimensional array to be accumulated.
    axis: integer axis along which to accumulate. If None (default), then
      array will be flattened and accumulated along the flattened axis.
    dtype: optionally specify the dtype of the output. If not specified,
      then the output dtype will match the input dtype.
    out: unused by JAX

  Returns:
    An array containing the accumulated sum along the given axis.

  See also:
    - :func:`jax.numpy.cumsum`: cumulative sum without ignoring NaN values.
    - :func:`jax.numpy.cumulative_sum`: cumulative sum via the array API standard.
    - :meth:`jax.numpy.add.accumulate`: cumulative sum via ufunc methods.
    - :func:`jax.numpy.sum`: sum along axis

  Examples:
    >>> x = jnp.array([[1., 2., jnp.nan],
    ...                [4., jnp.nan, 6.]])

    The standard cumulative sum will propagate NaN values:

    >>> jnp.cumsum(x)
    Array([ 1.,  3., nan, nan, nan, nan], dtype=float32)

    :func:`~jax.numpy.nancumsum` will ignore NaN values, effectively replacing
    them with zeros:

    >>> jnp.nancumsum(x)
    Array([ 1.,  3.,  3.,  7.,  7., 13.], dtype=float32)

    Cumulative sum along axis 1:

    >>> jnp.nancumsum(x, axis=1)
    Array([[ 1.,  3.,  3.],
           [ 4.,  4., 10.]], dtype=float32)
  """
  return _cumulative_reduction("nancumsum", control_flow.cumsum, a, axis, dtype, out,
                               fill_nan=True, fill_value=0)

