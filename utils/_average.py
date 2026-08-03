import math


def _average(a: ArrayLike, axis: Axis = None, weights: ArrayLike | None = None,
             returned: bool = False, keepdims: bool = False) -> Array | tuple[Array, Array]:
  axis_tuple = canonicalize_axis_tuple(axis, np.ndim(a))

  if weights is None: # Treat all weights as 1
    a = ensure_arraylike("average", a)
    a, = promote_dtypes_inexact(a)
    avg = mean(a, axis=axis, keepdims=keepdims)
    if axis is None:
      weights_sum = lax.full((), core.dimension_as_value(a.size), dtype=avg.dtype)
    else:
      weights_sum = lax.full((), math.prod(core.dimension_as_value(a.shape[d]) for d in axis_tuple), dtype=avg.dtype)
  else:
    a, weights = ensure_arraylike("average", a, weights)
    a, weights = promote_dtypes_inexact(a, weights)

    if a.shape != weights.shape:
      if axis is None:
        raise ValueError("Axis must be specified when shapes of a and "
                         "weights differ.")
      if weights.shape != tuple(a.shape[ax] for ax in axis_tuple):
        raise ValueError("Shape of weights must be consistent with shape "
                         "of a along specified axis.")
      new_shape = tuple(dim if i in axis_tuple else 1 for i, dim in enumerate(a.shape))
      weights = lax.reshape(weights, new_shape, dimensions=tuple(np.argsort(axis_tuple)))

    weights_sum = sum(weights, axis=axis, keepdims=keepdims)
    avg = sum(a * weights, axis=axis, keepdims=keepdims) / weights_sum

  if returned:
    if avg.shape != weights_sum.shape:
      weights_sum = _broadcast_to(weights_sum, avg.shape)
    return avg, weights_sum
  return avg

