
def _linspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
              endpoint: bool = True, retstep: bool = False,
              dtype: DTypeLike | None = None,
              axis: int = 0,
              *, device: xc.Device | Sharding | None = None) -> Array | tuple[Array, Array]:
  """Implementation of linspace differentiable in start and stop args."""
  if num < 0:
    raise ValueError(f"Number of samples, {num}, must be non-negative.")
  start, stop = util.ensure_arraylike("linspace", start, stop)

  if dtype is None:
    dtype = dtypes.to_inexact_dtype(dtypes.result_type(start, stop))
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "linspace")
  computation_dtype = dtypes.to_inexact_dtype(dtype)
  start = start.astype(computation_dtype)
  stop = stop.astype(computation_dtype)

  bounds_shape = list(lax.broadcast_shapes(np.shape(start), np.shape(stop)))
  broadcast_start = util._broadcast_to(start, bounds_shape)
  broadcast_stop = util._broadcast_to(stop, bounds_shape)
  axis = len(bounds_shape) + axis + 1 if axis < 0 else axis
  bounds_shape.insert(axis, 1)
  div = (num - 1) if endpoint else num
  if num > 1:
    delta: Array = lax.convert_element_type(stop - start, computation_dtype) / asarray(div, dtype=computation_dtype)
    iota_shape = [1,] * len(bounds_shape)
    iota_shape[axis] = div
    # This approach recovers the endpoints with float32 arithmetic,
    # but can lead to rounding errors for integer outputs.
    real_dtype = dtypes.finfo(computation_dtype).dtype
    step = lax.iota(real_dtype, div).reshape(iota_shape) / asarray(div, real_dtype)
    step = step.astype(computation_dtype)
    out = (broadcast_start.reshape(bounds_shape) * (1 - step) +
      broadcast_stop.reshape(bounds_shape) * step)

    if endpoint:
      out = lax.concatenate([out, lax.expand_dims(broadcast_stop, (axis,))],
                            canonicalize_axis(axis, out.ndim))

  elif num == 1:
    delta = asarray(np.nan if endpoint else stop - start, dtype=computation_dtype)
    out = broadcast_start.reshape(bounds_shape)
  else:  # num == 0 degenerate case, match numpy behavior
    empty_shape = list(lax.broadcast_shapes(np.shape(start), np.shape(stop)))
    empty_shape.insert(axis, 0)
    delta = full((), np.nan, computation_dtype)
    out = empty(empty_shape, dtype)

  if dtypes.issubdtype(dtype, np.integer) and not dtypes.issubdtype(out.dtype, np.integer):
    out = lax.floor(out)

  sharding = util.canonicalize_device_to_sharding(device)
  result = lax._convert_element_type(out, dtype, sharding=sharding)
  return (result, delta) if retstep else result

