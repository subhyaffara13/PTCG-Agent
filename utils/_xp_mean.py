
def _xp_mean(x, /, *, axis=None, weights=None, keepdims=False, nan_policy='propagate',
             dtype=None, warn=True, xp=None):
    r"""Compute the arithmetic mean along the specified axis.

    Parameters
    ----------
    x : real array
        Array containing real numbers whose mean is desired.
    axis : int or tuple of ints, default: None
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.
    weights : real array, optional
        If specified, an array of weights associated with the values in `x`;
        otherwise ``1``. If `weights` and `x` do not have the same shape, the
        arrays will be broadcasted before performing the calculation. See
        Notes for details.
    keepdims : bool, optional
        If this is set to ``True``, the axes which are reduced are left
        in the result as dimensions with length one. With this option,
        the result will broadcast correctly against the input array.
    nan_policy : {'propagate', 'omit', 'raise'}, default: 'propagate'
        Defines how to handle input NaNs.

        - ``propagate``: if a NaN is present in the axis slice (e.g. row) along
          which the statistic is computed, the corresponding entry of the output
          will be NaN.
        - ``omit``: NaNs will be omitted when performing the calculation.
          If insufficient data remains in the axis slice along which the
          statistic is computed, the corresponding entry of the output will be
          NaN.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    dtype : dtype, optional
        Type to use in computing the mean. For integer inputs, the default is
        the default float type of the array library; for floating point inputs,
        the dtype is that of the input.

    Returns
    -------
    out : array
        The mean of each slice

    Notes
    -----
    Let :math:`x_i` represent element :math:`i` of data `x` and let :math:`w_i`
    represent the corresponding element of `weights` after broadcasting. Then the
    (weighted) mean :math:`\bar{x}_w` is given by:

    .. math::

        \bar{x}_w = \frac{ \sum_{i=0}^{n-1} w_i x_i }
                         { \sum_{i=0}^{n-1} w_i }

    where :math:`n` is the number of elements along a slice. Note that this simplifies
    to the familiar :math:`(\sum_i x_i) / n` when the weights are all ``1`` (default).

    The behavior of this function with respect to weights is somewhat different
    from that of `np.average`. For instance,
    `np.average` raises an error when `axis` is not specified and the shapes of `x`
    and the `weights` array are not the same; `xp_mean` simply broadcasts the two.
    Also, `np.average` raises an error when weights sum to zero along a slice;
    `xp_mean` computes the appropriate result. The intent is for this function's
    interface to be consistent with the rest of `scipy.stats`.

    Note that according to the formula, including NaNs with zero weights is not
    the same as *omitting* NaNs with ``nan_policy='omit'``; in the former case,
    the NaNs will continue to propagate through the calculation whereas in the
    latter case, the NaNs are excluded entirely.

    """
    # ensure that `x` and `weights` are array-API compatible arrays of identical shape
    xp = array_namespace(x) if xp is None else xp
    x = _asarray(x, dtype=dtype, subok=True)
    weights = xp.asarray(weights, dtype=dtype) if weights is not None else weights

    # to ensure that this matches the behavior of decorated functions when one of the
    # arguments has size zero, it's easiest to call a similar decorated function.
    if is_numpy(xp) and (xp_size(x) == 0
                         or (weights is not None and xp_size(weights) == 0)):
        return gmean(x, weights=weights, axis=axis, keepdims=keepdims)

    x, weights = xp_promote(x, weights, broadcast=True, force_floating=True, xp=xp)
    if weights is not None:
        x, weights = _share_masks(x, weights, xp=xp)

    # handle the special case of zero-sized arrays
    message = (too_small_1d_not_omit if (x.ndim == 1 or axis is None)
               else too_small_nd_not_omit)
    if xp_size(x) == 0:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = xp.mean(x, axis=axis, keepdims=keepdims)
        if warn and xp_size(res) != 0:
            warnings.warn(message, SmallSampleWarning, stacklevel=2)
        return res

    contains_nan = _contains_nan(x, nan_policy, xp_omit_okay=True, xp=xp)
    if weights is not None:
        contains_nan_w = _contains_nan(weights, nan_policy, xp_omit_okay=True, xp=xp)
        contains_nan = contains_nan | contains_nan_w

    # Handle `nan_policy='omit'` by giving zero weight to NaNs, whether they
    # appear in `x` or `weights`. Emit warning if there is an all-NaN slice.
    # Test nan_policy before the implicit call to bool(contains_nan)
    # to avoid raising on lazy xps on the default nan_policy='propagate'
    lazy = is_lazy_array(x)
    if nan_policy == 'omit' and (lazy or contains_nan):
        nan_mask = xp.isnan(x)
        if weights is not None:
            nan_mask |= xp.isnan(weights)
        if warn and not lazy and xp.any(xp.all(nan_mask, axis=axis)):
            message = (too_small_1d_omit if (x.ndim == 1 or axis is None)
                       else too_small_nd_omit)
            warnings.warn(message, SmallSampleWarning, stacklevel=2)
        weights = xp.ones_like(x) if weights is None else weights
        x = xp.where(nan_mask, 0., x)
        weights = xp.where(nan_mask, 0., weights)

    # Perform the mean calculation itself
    if weights is None:
        return xp.mean(x, axis=axis, keepdims=keepdims)

    # consider using `vecdot` if `axis` tuple support is added (data-apis/array-api#910)
    norm = xp.sum(weights, axis=axis)
    wsum = xp.sum(x * weights, axis=axis)
    with np.errstate(divide='ignore', invalid='ignore'):
        res = wsum/norm

    # Respect `keepdims` and convert NumPy 0-D arrays to scalars
    if keepdims:

        if axis is None:
            final_shape = (1,) * len(x.shape)
        else:
            # axis can be a scalar or sequence
            axes = (axis,) if not isinstance(axis, Sequence) else axis
            final_shape = list(x.shape)
            for i in axes:
                final_shape[i] = 1

        res = xp.reshape(res, tuple(final_shape))

    return res[()] if res.ndim == 0 else res

