
def _logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None, *, xp):
    if not isinstance(base, float | int) and xp.asarray(base).ndim > 0:
        # If base is non-scalar, broadcast it with the others, since it
        # may influence how axis is interpreted.
        start, stop, base = map(xp.asarray, (start, stop, base))
        ndmax = xp.broadcast_arrays(start, stop, base).ndim
        start, stop, base = (
            xpx.atleast_nd(a, ndim=ndmax)
            for a in (start, stop, base)
        )
        base = xp.expand_dims(base)
    try:
        result_dt = xp.result_type(start, stop, base)
    except ValueError:
        # all of start, stop and base are python scalars
        result_dt = xp_default_dtype(xp)
    y = xp.linspace(start, stop, num=num, endpoint=endpoint, dtype=result_dt)

    yp = xp.pow(base, y)
    if dtype is None:
        return yp
    return xp.astype(yp, dtype, copy=False)


def _logspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
              endpoint: bool = True, base: ArrayLike = 10.0,
              dtype: DTypeLike | None = None, axis: int = 0) -> Array:
  """Implementation of logspace differentiable in start and stop args."""
  if dtype is None:
    dtype = dtypes.to_inexact_dtype(dtypes.result_type(start, stop))
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "logspace")
  computation_dtype = dtypes.to_inexact_dtype(dtype)
  start, stop = util.ensure_arraylike("logspace", start, stop)
  start = start.astype(computation_dtype)
  stop = stop.astype(computation_dtype)
  lin = linspace(start, stop, num,
                 endpoint=endpoint, retstep=False, dtype=None, axis=axis)
  return lax.convert_element_type(ufuncs.power(base, lin), dtype)

