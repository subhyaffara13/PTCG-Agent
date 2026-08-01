
def percentile(
    a: ArrayLike,
    q: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    overwrite_input=False,
    method="linear",
    keepdims: KeepDims = False,
    *,
    interpolation: NotImplementedType = None,
):
    # np.percentile(float_tensor, 30) : q.dtype is int64 => q / 100.0 is float32
    if _dtypes_impl.python_type_for_torch(q.dtype) is int:
        q = q.to(_dtypes_impl.default_dtypes().float_dtype)
    qq = q / 100.0

    return quantile(
        a,
        qq,
        axis=axis,
        overwrite_input=overwrite_input,
        method=method,
        keepdims=keepdims,
        interpolation=interpolation,
    )


def percentile(a,
               q,
               axis=None,
               out=None,
               overwrite_input=False,
               method="linear",
               keepdims=False,
               *,
               weights=None):
    """
    Compute the q-th percentile of the data along the specified axis.

    Returns the q-th percentile(s) of the array elements.

    Parameters
    ----------
    a : array_like of real numbers
        Input array or object that can be converted to an array.
    q : array_like of float
        Percentage or sequence of percentages for the percentiles to compute.
        Values must be between 0 and 100 inclusive.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the percentiles are computed. The
        default is to compute the percentile(s) along a flattened
        version of the array.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output,
        but the type (of the output) will be cast if necessary.
    overwrite_input : bool, optional
        If True, then allow the input array `a` to be modified by intermediate
        calculations, to save memory. In this case, the contents of the input
        `a` after this function completes is undefined.
    method : str, optional
        This parameter specifies the method to use for estimating the
        percentile.  There are many different methods, some unique to NumPy.
        See the notes for explanation.  The options sorted by their R type
        as summarized in the H&F paper [1]_ are:

        1. 'inverted_cdf'
        2. 'averaged_inverted_cdf'
        3. 'closest_observation'
        4. 'interpolated_inverted_cdf'
        5. 'hazen'
        6. 'weibull'
        7. 'linear'  (default)
        8. 'median_unbiased'
        9. 'normal_unbiased'

        The first three methods are discontinuous.  NumPy further defines the
        following discontinuous variations of the default 'linear' (7.) option:

        * 'lower'
        * 'higher',
        * 'midpoint'
        * 'nearest'

        .. versionchanged:: 1.22.0
            This argument was previously called "interpolation" and only
            offered the "linear" default and last four options.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left in
        the result as dimensions with size one. With this option, the
        result will broadcast correctly against the original array `a`.

    weights : array_like, optional
        An array of weights associated with the values in `a`. Each value in
        `a` contributes to the percentile according to its associated weight.
        The weights array can either be 1-D (in which case its length must be
        the size of `a` along the given axis) or of the same shape as `a`.
        If `weights=None`, then all data in `a` are assumed to have a
        weight equal to one.
        Only `method="inverted_cdf"` supports weights.
        See the notes for more details.

        .. versionadded:: 2.0.0

    Returns
    -------
    percentile : scalar or ndarray
        If `q` is a single percentile and `axis=None`, then the result
        is a scalar. If multiple percentiles are given, first axis of
        the result corresponds to the percentiles. The other axes are
        the axes that remain after the reduction of `a`. If the input
        contains integers or floats smaller than ``float64``, the output
        data-type is ``float64``. Otherwise, the output data-type is the
        same as that of the input. If `out` is specified, that array is
        returned instead.

    See Also
    --------
    mean
    median : equivalent to ``percentile(..., 50)``
    nanpercentile
    quantile : equivalent to percentile, except q in the range [0, 1].

    Notes
    -----
    The behavior of `numpy.percentile` with percentage `q` is
    that of `numpy.quantile` with argument ``q/100``.
    For more information, please see `numpy.quantile`.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[10, 7, 4], [3, 2, 1]])
    >>> a
    array([[10,  7,  4],
           [ 3,  2,  1]])
    >>> np.percentile(a, 50)
    3.5
    >>> np.percentile(a, 50, axis=0)
    array([6.5, 4.5, 2.5])
    >>> np.percentile(a, 50, axis=1)
    array([7.,  2.])
    >>> np.percentile(a, 50, axis=1, keepdims=True)
    array([[7.],
           [2.]])

    >>> m = np.percentile(a, 50, axis=0)
    >>> out = np.zeros_like(m)
    >>> np.percentile(a, 50, axis=0, out=out)
    array([6.5, 4.5, 2.5])
    >>> m
    array([6.5, 4.5, 2.5])

    >>> b = a.copy()
    >>> np.percentile(b, 50, axis=1, overwrite_input=True)
    array([7.,  2.])
    >>> assert not np.all(a == b)

    The different methods can be visualized graphically:

    .. plot::

        import matplotlib.pyplot as plt

        a = np.arange(4)
        p = np.linspace(0, 100, 6001)
        ax = plt.gca()
        lines = [
            ('linear', '-', 'C0'),
            ('inverted_cdf', ':', 'C1'),
            # Almost the same as `inverted_cdf`:
            ('averaged_inverted_cdf', '-.', 'C1'),
            ('closest_observation', ':', 'C2'),
            ('interpolated_inverted_cdf', '--', 'C1'),
            ('hazen', '--', 'C3'),
            ('weibull', '-.', 'C4'),
            ('median_unbiased', '--', 'C5'),
            ('normal_unbiased', '-.', 'C6'),
            ]
        for method, style, color in lines:
            ax.plot(
                p, np.percentile(a, p, method=method),
                label=method, linestyle=style, color=color)
        ax.set(
            title='Percentiles for different methods and data: ' + str(a),
            xlabel='Percentile',
            ylabel='Estimated percentile value',
            yticks=a)
        ax.legend(bbox_to_anchor=(1.03, 1))
        plt.tight_layout()
        plt.show()

    References
    ----------
    .. [1] R. J. Hyndman and Y. Fan,
       "Sample quantiles in statistical packages,"
       The American Statistician, 50(4), pp. 361-365, 1996

    """
    a = np.asanyarray(a)
    if a.dtype.kind == "c":
        raise TypeError("a must be an array of real numbers")

    weak_q = type(q) in (int, float)  # use weak promotion for final result type
    q = np.true_divide(q, 100, out=...)
    if not _quantile_is_valid(q):
        raise ValueError("Percentiles must be in the range [0, 100]")

    if weights is not None:
        if method != "inverted_cdf":
            msg = ("Only method 'inverted_cdf' supports weights. "
                   f"Got: {method}.")
            raise ValueError(msg)
        if axis is not None:
            axis = _nx.normalize_axis_tuple(axis, a.ndim, argname="axis")
        weights = _weights_are_valid(weights=weights, a=a, axis=axis)
        if np.any(weights < 0):
            raise ValueError("Weights must be non-negative.")

    return _quantile_unchecked(
        a, q, axis, out, overwrite_input, method, keepdims, weights, weak_q)


def percentile(a: ArrayLike, q: ArrayLike,
               axis: int | tuple[int, ...] | None = None,
               out: None = None, overwrite_input: bool = False, method: str = "linear",
               keepdims: bool = False, *, weights: ArrayLike | None = None,
               out_sharding: NamedSharding | P | None = None) -> Array:
  """Compute the percentile of the data along the specified axis.

  JAX implementation of :func:`numpy.percentile`.

  Args:
    a: N-dimensional array input.
    q: scalar or 1-dimensional array specifying the desired quantiles. ``q``
      should contain integer or floating point values between ``0`` and ``100``.
    axis: optional axis or tuple of axes along which to compute the quantile
    out: not implemented by JAX; will error if not None
    overwrite_input: not implemented by JAX; will error if not False
    method: specify the interpolation method to use. Options are one of
      ``["linear", "lower", "higher", "midpoint", "nearest"]``.
      default is ``linear``.
    keepdims: if True, then the returned array will have the same number of
      dimensions as the input. Default is False.
    weights: keyword-only. optional array of weights for each element in `a`.
      Values with higher weights contribute more to the percentile calculation.
      The weights array must be broadcastable to the shape of `a` along the specified axis.
      Currently, weighted percentiles are only supported when `method="inverted_cdf"`.

  Returns:
    An array containing the specified percentiles along the specified axes.

  See also:
    - :func:`jax.numpy.quantile`: compute the quantile (0.0-1.0)
    - :func:`jax.numpy.nanpercentile`: compute the percentile while ignoring NaNs

  Examples:
    Computing the median and quartiles of a 1D array:

    >>> x = jnp.array([0, 1, 2, 3, 4, 5, 6])
    >>> q = jnp.array([25, 50, 75])
    >>> jnp.percentile(x, q)
    Array([1.5, 3. , 4.5], dtype=float32)

    Computing the same percentiles with nearest rather than linear interpolation:

    >>> jnp.percentile(x, q, method='nearest')
    Array([1., 3., 4.], dtype=float32)

    Computing weighted percentiles:

    >>> x = jnp.array([1, 2, 3, 4, 5])
    >>> weights = jnp.array([1, 1, 2, 1, 1])
    >>> jnp.percentile(x, 50, weights=weights, method='inverted_cdf')
    Array(3., dtype=float32)
  """
  a, q = ensure_arraylike("percentile", a, q)
  if weights is not None:
    weights = ensure_arraylike("percentile", weights)
  q, = promote_dtypes_inexact(q)
  def internal_quantile(x, y, w):
    return quantile(x, y, axis=axis, out=out, overwrite_input=overwrite_input,
                    method=method, keepdims=keepdims, weights=w)
  if out_sharding is not None:
    assert isinstance(out_sharding, (NamedSharding, P))
    out_sharding = canonicalize_sharding(out_sharding, 'jnp.percentile')
    return auto_axes(internal_quantile, out_sharding=out_sharding,
                     axes=out_sharding.mesh.explicit_axes
                     )(a, q / 100, weights)
  return internal_quantile(a, q / 100, weights)

