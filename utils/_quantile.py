import math


def _quantile(
    arr: "np.typing.ArrayLike",
    quantiles: np.ndarray,
    axis: int = -1,
    method: str = "linear",
    out: np.ndarray | None = None,
    weights: "np.typing.ArrayLike | None" = None,
    weak_q: bool = False,
) -> np.ndarray:
    """
    Private function that doesn't support extended axis or keepdims.
    These methods are extended to this function using _ureduce.
    See nanpercentile for parameter usage.
    It computes the quantiles of the array for the given axis.
    A linear interpolation is performed based on the `method`.

    By default, the method is "linear" where alpha == beta == 1 which
    performs the 7th method of Hyndman&Fan.
    With "median_unbiased" we get alpha == beta == 1/3
    thus the 8th method of Hyndman&Fan.
    """
    # --- Setup
    arr = np.asanyarray(arr)
    values_count = arr.shape[axis]
    # The dimensions of `q` are prepended to the output shape, so we need the
    # axis being sampled from `arr` to be last.
    if axis != 0:  # But moveaxis is slow, so only call it if necessary.
        arr = np.moveaxis(arr, axis, destination=0)
    supports_nans = (
        np.issubdtype(arr.dtype, np.inexact) or arr.dtype.kind in 'Mm'
    )

    if weights is None:
        # --- Computation of indexes
        # Index where to find the value in the sorted array.
        # Virtual because it is a floating point value, not a valid index.
        # The nearest neighbours are used for interpolation
        try:
            method_props = _QuantileMethods[method]
        except KeyError:
            raise ValueError(
                f"{method!r} is not a valid method. Use one of: "
                f"{_QuantileMethods.keys()}") from None
        virtual_indexes = method_props["get_virtual_index"](values_count,
                                                            quantiles)
        virtual_indexes = np.asanyarray(virtual_indexes)

        if method_props["fix_gamma"] is None:
            supports_integers = True
        else:
            int_virtual_indices = np.issubdtype(virtual_indexes.dtype,
                                                np.integer)
            supports_integers = method == 'linear' and int_virtual_indices

        if supports_integers:
            # No interpolation needed, take the points along axis
            if supports_nans:
                # may contain nan, which would sort to the end
                arr.partition(
                    concatenate((virtual_indexes.ravel(), [-1])), axis=0,
                )
                slices_having_nans = np.isnan(arr[-1, ...])
            else:
                # cannot contain nan
                arr.partition(virtual_indexes.ravel(), axis=0)
                slices_having_nans = np.array(False, dtype=bool)
            result = take(arr, virtual_indexes, axis=0, out=out)
        else:
            previous_indexes, next_indexes = _get_indexes(arr,
                                                          virtual_indexes,
                                                          values_count)
            # --- Sorting
            arr.partition(
                np.unique(np.concatenate(([0, -1],
                                          previous_indexes.ravel(),
                                          next_indexes.ravel(),
                                          ))),
                axis=0)
            if supports_nans:
                slices_having_nans = np.isnan(arr[-1, ...])
            else:
                slices_having_nans = None
            # --- Get values from indexes
            previous = arr[previous_indexes]
            next = arr[next_indexes]
            # --- Linear interpolation
            gamma = _get_gamma(virtual_indexes, previous_indexes,
                               method_props)
            if weak_q:
                gamma = float(gamma)
            else:
                result_shape = virtual_indexes.shape + (1,) * (arr.ndim - 1)
                gamma = gamma.reshape(result_shape)
            result = _lerp(previous,
                        next,
                        gamma,
                        out=out)
    else:
        # Weighted case
        # This implements method="inverted_cdf", the only supported weighted
        # method, which needs to sort anyway.
        weights = np.asanyarray(weights)
        if axis != 0:
            weights = np.moveaxis(weights, axis, destination=0)
        index_array = np.argsort(arr, axis=0)

        # arr = arr[index_array, ...]  # but this adds trailing dimensions of
        # 1.
        arr = np.take_along_axis(arr, index_array, axis=0)
        if weights.shape == arr.shape:
            weights = np.take_along_axis(weights, index_array, axis=0)
        else:
            # weights is 1d
            weights = weights.reshape(-1)[index_array, ...]

        if supports_nans:
            # may contain nan, which would sort to the end
            slices_having_nans = np.isnan(arr[-1, ...])
        else:
            # cannot contain nan
            slices_having_nans = np.array(False, dtype=bool)

        # We use the weights to calculate the empirical cumulative
        # distribution function cdf
        cdf = weights.cumsum(axis=0, dtype=np.float64)
        cdf /= cdf[-1, ...]  # normalization to 1
        if np.isnan(cdf[-1]).any():
            # Above calculations should normally warn for the zero/inf case.
            raise ValueError("Weights included NaN, inf or were all zero.")
        # Search index i such that
        #   sum(weights[j], j=0..i-1) < quantile <= sum(weights[j], j=0..i)
        # is then equivalent to
        #   cdf[i-1] < quantile <= cdf[i]
        # Unfortunately, searchsorted only accepts 1-d arrays as first
        # argument, so we will need to iterate over dimensions.

        # Without the following cast, searchsorted can return surprising
        # results, e.g.
        #   np.searchsorted(np.array([0.2, 0.4, 0.6, 0.8, 1.]),
        #                   np.array(0.4, dtype=np.float32), side="left")
        # returns 2 instead of 1 because 0.4 is not binary representable.
        if quantiles.dtype.kind == "f":
            cdf = cdf.astype(quantiles.dtype)
        # Weights must be non-negative, so we might have zero weights at the
        # beginning leading to some leading zeros in cdf. The call to
        # np.searchsorted for quantiles=0 will then pick the first element,
        # but should pick the first one larger than zero. We
        # therefore simply set 0 values in cdf to -1.
        if np.any(cdf[0, ...] == 0):
            cdf[cdf == 0] = -1

        def find_cdf_1d(arr, cdf):
            indices = np.searchsorted(cdf, quantiles, side="left")
            # We might have reached the maximum with i = len(arr), e.g. for
            # quantiles = 1, and need to cut it to len(arr) - 1.
            indices = minimum(indices, values_count - 1)
            result = take(arr, indices, axis=0)
            return result

        r_shape = arr.shape[1:]
        if quantiles.ndim > 0:
            r_shape = quantiles.shape + r_shape
        if out is None:
            result = np.empty_like(arr, shape=r_shape)
        else:
            if out.shape != r_shape:
                msg = (f"Wrong shape of argument 'out', shape={r_shape} is "
                       f"required; got shape={out.shape}.")
                raise ValueError(msg)
            result = out

        # See apply_along_axis, which we do for axis=0. Note that Ni = (,)
        # always, so we remove it here.
        Nk = arr.shape[1:]
        for kk in np.ndindex(Nk):
            result[(...,) + kk] = find_cdf_1d(
                arr[np.s_[:, ] + kk], cdf[np.s_[:, ] + kk]
            )

        # Make result the same as in unweighted inverted_cdf.
        if result.shape == () and result.dtype == np.dtype("O"):
            result = result.item()

    if np.any(slices_having_nans):
        if result.ndim == 0 and out is None:
            # can't write to a scalar, but indexing will be correct
            result = arr[-1]
        else:
            np.copyto(result, arr[-1, ...], where=slices_having_nans)
    return result


def _quantile(a: Array, q: Array, axis: int | tuple[int, ...] | None,
              method: str, keepdims: bool, squash_nans: bool, weights: Array | None = None) -> Array:
  if method not in ["linear", "lower", "higher", "midpoint", "nearest", "inverted_cdf"]:
    raise ValueError("method can only be 'linear', 'lower', 'higher', 'midpoint', 'nearest' or 'inverted_cdf'")
  if weights is not None:
    if dtypes.issubdtype(weights.dtype, np.complexfloating):
      raise ValueError("Weights cannot be complex types.")
    if method != "inverted_cdf":
      raise NotImplementedError(f"{method} doesn't support weights. Only method 'inverted_cdf' supports weights.")
    a, weights = promote_dtypes_inexact(a, weights)
    if weights.shape != a.shape:
      if axis is None:
        raise ValueError("Weights shape must match 'a' shape when axis is None.")
      ax_tuple = canonicalize_axis_tuple(axis, a.ndim)
      if weights.shape != tuple(a.shape[ax] for ax in ax_tuple):
        raise ValueError(f"Weights shape {weights.shape} must match reduction axes "
                          f"{tuple(a.shape[ax] for ax in ax_tuple)}")
      weights = lax.broadcast_in_dim(weights, a.shape, broadcast_dimensions=ax_tuple)
  else:
    a, = promote_dtypes_inexact(a)
  keepdim = []
  if dtypes.issubdtype(a.dtype, np.complexfloating):
    raise ValueError("quantile does not support complex input, as the operation is poorly defined.")
  if axis is None:
    if keepdims:
      keepdim = [1] * a.ndim
    a = a.ravel()
    if weights is not None:
      weights = weights.ravel()
    axis = 0
  elif isinstance(axis, tuple):
    keepdim = list(a.shape)
    nd = a.ndim
    axis = tuple(canonicalize_axis(ax, nd) for ax in axis)
    if len(set(axis)) != len(axis):
      raise ValueError('repeated axis')
    for ax in axis:
      keepdim[ax] = 1

    keep = set(range(nd)) - set(axis)
    # prepare permutation
    dimensions = list(range(nd))
    for i, s in enumerate(sorted(keep)):
      dimensions[i], dimensions[s] = dimensions[s], dimensions[i]
    do_not_touch_shape = tuple(x for idx,x in enumerate(a.shape) if idx not in axis)
    touch_shape = tuple(x for idx,x in enumerate(a.shape) if idx in axis)
    a = lax.reshape(a, do_not_touch_shape + (math.prod(touch_shape),), dimensions)
    if weights is not None:
      weights = lax.reshape(weights, do_not_touch_shape + (math.prod(touch_shape),), dimensions)
    axis = canonicalize_axis(-1, a.ndim)
  else:
    axis = canonicalize_axis(axis, a.ndim)

  q_shape = q.shape
  q_ndim = q.ndim
  if q_ndim > 1:
    raise ValueError(f"q must be have rank <= 1, got shape {q.shape}")

  a_shape = a.shape
  q_orig = q
  if squash_nans:
    a = _where(lax._isnan(a), np.nan, a) # Ensure nans are positive so they sort to the end.
    if weights is not None:
      a, weights = lax.sort_key_val(a, weights, dimension=axis)
    else:
      a = lax.sort(a, dimension=axis)
    counts = sum(lax.bitwise_not(lax._isnan(a)), axis=axis, dtype=q.dtype, keepdims=keepdims)
    shape_after_reduction = counts.shape
    q = lax.expand_dims(
      q, tuple(range(q_ndim, len(shape_after_reduction) + q_ndim)))
    counts = lax.expand_dims(counts, tuple(range(q_ndim)))
    q = lax.mul(q, lax.sub(counts, lax._const(q, 1)))
    low = lax.floor(q)
    high = lax.ceil(q)
    high_weight = lax.sub(q, low)
    low_weight = lax.sub(lax._const(high_weight, 1), high_weight)

    low = lax.max(lax._const(low, 0), lax.min(low, counts - 1))
    high = lax.max(lax._const(high, 0), lax.min(high, counts - 1))
    low = lax.convert_element_type(low, int)
    high = lax.convert_element_type(high, int)
    out_shape = q_shape + shape_after_reduction
    index = [lax.broadcasted_iota(int, out_shape, dim + q_ndim)
             for dim in range(len(shape_after_reduction))]
    if keepdims:
      index[axis] = low
    else:
      index.insert(axis, low)
    low_value = a[tuple(index)]
    index[axis] = high
    high_value = a[tuple(index)]
  else:
    with config.debug_nans(False):
      a = _where(any(lax._isnan(a), axis=axis, keepdims=True), np.nan, a)
    if weights is not None:
      a, weights = lax.sort_key_val(a, weights, dimension=axis)
    else:
      a = lax.sort(a, dimension=axis)
    n = lax.convert_element_type(a_shape[axis], lax._dtype(q))
    q = lax.mul(q, n - 1)
    low = lax.floor(q)
    high = lax.ceil(q)
    high_weight = lax.sub(q, low)
    low_weight = lax.sub(lax._const(high_weight, 1), high_weight)

    low = lax.clamp(lax._const(low, 0), low, n - 1)
    high = lax.clamp(lax._const(high, 0), high, n - 1)
    low = lax.convert_element_type(low, int)
    high = lax.convert_element_type(high, int)

    slice_sizes = list(a_shape)
    slice_sizes[axis] = 1
    dnums = lax_slicing.GatherDimensionNumbers(
      offset_dims=tuple(range(
        q_ndim,
        len(a_shape) + q_ndim if keepdims else len(a_shape) + q_ndim - 1)),
      collapsed_slice_dims=() if keepdims else (axis,),
      start_index_map=(axis,))
    low_value = lax_slicing.gather(a, low[..., None], dimension_numbers=dnums,
                                   slice_sizes=slice_sizes)
    high_value = lax_slicing.gather(a, high[..., None], dimension_numbers=dnums,
                                    slice_sizes=slice_sizes)
    if q_ndim == 1:
      low_weight = lax.broadcast_in_dim(low_weight, low_value.shape,
                                        broadcast_dimensions=(0,))
      high_weight = lax.broadcast_in_dim(high_weight, high_value.shape,
                                        broadcast_dimensions=(0,))

  if method == "linear":
    result = lax.add(lax.mul(low_value.astype(q.dtype), low_weight),
                     lax.mul(high_value.astype(q.dtype), high_weight))
  elif method == "lower":
    result = low_value
  elif method == "higher":
    result = high_value
  elif method == "nearest":
    pred = lax.le(high_weight, lax._const(high_weight, 0.5))
    result = lax.select(pred, low_value, high_value)
  elif method == "midpoint":
    result = lax.mul(lax.add(low_value, high_value), lax._const(low_value, 0.5))
  elif method == "inverted_cdf":
    if weights is None:
      weights = lax.full_like(a, 1.0)
    zeros = lax.full_like(weights, 0)
    bad_weights = lax.bitwise_or(lax.lt(weights, zeros), lax._isnan(weights))
    nan_data = lax._isnan(a)
    clean_weights = lax.select(lax.bitwise_or(bad_weights, nan_data), zeros, weights)
    cum_weights = cumsum(clean_weights, axis=axis)
    total_weight = lax_slicing.index_in_dim(cum_weights, -1, axis=axis, keepdims=keepdims)
    tw_f = lax.expand_dims(total_weight, tuple(range(q_ndim)))
    q_f = lax.reshape(q_orig, q_orig.shape + (1,) * total_weight.ndim)
    target_w = lax.mul(q_f, tw_f)
    target_w_aligned = target_w if keepdims else lax.expand_dims(target_w, (axis + q_ndim,))
    cw_f = lax.expand_dims(cum_weights, tuple(range(q_ndim)))
    is_less = lax.lt(cw_f, target_w_aligned)
    idx = sum(lax.convert_element_type(is_less, dtypes.default_int_dtype()), axis=axis + q_ndim, keepdims=keepdims)
    if squash_nans:
      valid_counts = sum(lax.bitwise_not(nan_data), axis=axis, dtype=q.dtype, keepdims=keepdims)
    else:
      valid_counts = lax.full_like(total_weight, a_shape[axis], dtype=q.dtype)
    limit = lax.sub(valid_counts, lax._const(valid_counts, 1))
    max_idx = lax.convert_element_type(limit, dtypes.default_int_dtype())
    max_idx_f = lax.expand_dims(max_idx, tuple(range(q_ndim)))
    max_idx_f = lax.convert_element_type(max_idx_f, idx.dtype)
    idx = lax.max(lax._const(idx, 0), lax.min(idx, max_idx_f))
    if keepdims:
      idx_take = lax.squeeze(idx, (q_ndim + axis,))
    else:
      idx_take = idx
    if q_ndim == 0:
      idx_transposed = lax.expand_dims(idx_take, (axis,))
      result = indexing.take_along_axis(a, idx_transposed, axis=axis)
      result = lax.squeeze(result, (axis,))
    else:
      perm = [*range(q_ndim, q_ndim + axis),
              *range(q_ndim),
              *range(q_ndim + axis, idx_take.ndim)]
      idx_transposed = lax.transpose(idx_take, perm)
      result = indexing.take_along_axis(a, idx_transposed, axis=axis)
      inv_perm = [perm.index(i) for i in range(len(perm))]
      result = lax.transpose(result, inv_perm)
    if keepdims:
      result = lax.expand_dims(result, (q_ndim + axis,))
    all_nan_data = lax.eq(valid_counts, lax.full_like(valid_counts, 0))
    any_bad_weight = any(bad_weights, axis=axis, keepdims=keepdims)
    if squash_nans:
      force_nan = lax.bitwise_or(any_bad_weight, all_nan_data)
    else:
      force_nan = lax.bitwise_or(any_bad_weight, any(nan_data, axis=axis, keepdims=keepdims))
    force_nan_f = lax.expand_dims(force_nan, tuple(range(q_ndim)))
    result = _where(force_nan_f, lax.full_like(result, np.nan), result)
  else:
    raise ValueError(f"{method=!r} not recognized")
  if keepdims and keepdim:
    if q_ndim > 0:
      keepdim = [np.shape(q)[0], *keepdim]
    result = result.reshape(keepdim)
  return lax.convert_element_type(result, a.dtype)

