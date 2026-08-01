
def nancumprod(a, axis=None, dtype=None, out=None):
    """
    Return the cumulative product of array elements over a given axis treating Not a
    Numbers (NaNs) as one.  The cumulative product does not change when NaNs are
    encountered and leading NaNs are replaced by ones.

    Ones are returned for slices that are all-NaN or empty.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int, optional
        Axis along which the cumulative product is computed.  By default
        the input is flattened.
    dtype : dtype, optional
        Type of the returned array, as well as of the accumulator in which
        the elements are multiplied.  If *dtype* is not specified, it
        defaults to the dtype of `a`, unless `a` has an integer dtype with
        a precision less than that of the default platform integer.  In
        that case, the default platform integer is used instead.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output
        but the type of the resulting values will be cast if necessary.

    Returns
    -------
    nancumprod : ndarray
        A new array holding the result is returned unless `out` is
        specified, in which case it is returned.

    See Also
    --------
    numpy.cumprod : Cumulative product across array propagating NaNs.
    isnan : Show which elements are NaN.

    Examples
    --------
    >>> import numpy as np
    >>> np.nancumprod(1)
    array([1])
    >>> np.nancumprod([1])
    array([1])
    >>> np.nancumprod([1, np.nan])
    array([1.,  1.])
    >>> a = np.array([[1, 2], [3, np.nan]])
    >>> np.nancumprod(a)
    array([1.,  2.,  6.,  6.])
    >>> np.nancumprod(a, axis=0)
    array([[1.,  2.],
           [3.,  2.]])
    >>> np.nancumprod(a, axis=1)
    array([[1.,  2.],
           [3.,  3.]])

    """
    a, mask = _replace_nan(a, 1)
    return np.cumprod(a, axis=axis, dtype=dtype, out=out)


def nancumprod(a: ArrayLike, axis: int | None = None,
               dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative product of elements along an axis, ignoring NaN values.

  JAX implementation of :func:`numpy.nancumprod`.

  Args:
    a: N-dimensional array to be accumulated.
    axis: integer axis along which to accumulate. If None (default), then
      array will be flattened and accumulated along the flattened axis.
    dtype: optionally specify the dtype of the output. If not specified,
      then the output dtype will match the input dtype.
    out: unused by JAX

  Returns:
    An array containing the accumulated product along the given axis.

  See also:
    - :func:`jax.numpy.cumprod`: cumulative product without ignoring NaN values.
    - :meth:`jax.numpy.multiply.accumulate`: cumulative product via ufunc methods.
    - :func:`jax.numpy.prod`: product along axis

  Examples:
    >>> x = jnp.array([[1., 2., jnp.nan],
    ...                [4., jnp.nan, 6.]])

    The standard cumulative product will propagate NaN values:

    >>> jnp.cumprod(x)
    Array([ 1.,  2., nan, nan, nan, nan], dtype=float32)

    :func:`~jax.numpy.nancumprod` will ignore NaN values, effectively replacing
    them with ones:

    >>> jnp.nancumprod(x)
    Array([ 1.,  2.,  2.,  8.,  8., 48.], dtype=float32)

    Cumulative product along axis 1:

    >>> jnp.nancumprod(x, axis=1)
    Array([[ 1.,  2.,  2.],
           [ 4.,  4., 24.]], dtype=float32)
  """
  return _cumulative_reduction("nancumprod", control_flow.cumprod, a, axis, dtype, out,
                               fill_nan=True, fill_value=1)

