
def _geomspace(start: ArrayLike, stop: ArrayLike, num: int = 50, endpoint: bool = True,
               dtype: DTypeLike | None = None, axis: int = 0) -> Array:
  """Implementation of geomspace differentiable in start and stop args."""
  if dtype is None:
    dtype = dtypes.to_inexact_dtype(dtypes.result_type(start, stop))
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "geomspace")
  computation_dtype = dtypes.to_inexact_dtype(dtype)
  start, stop = util.ensure_arraylike("geomspace", start, stop)
  start = start.astype(computation_dtype)
  stop = stop.astype(computation_dtype)

  sign = ufuncs.sign(start)
  res = sign * logspace(ufuncs.log10(start / sign), ufuncs.log10(stop / sign),
                        num, endpoint=endpoint, base=10.0,
                        dtype=computation_dtype, axis=0)
  axis = canonicalize_axis(axis, res.ndim)
  if axis != 0:
    # res = moveaxis(res, 0, axis)
    res = lax.transpose(res, permutation=(*range(1, axis + 1), 0, *range(axis + 1, res.ndim)))
  return lax.convert_element_type(res, dtype)

