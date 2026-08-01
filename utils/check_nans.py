
def check_nans(prim, error, enabled_errors, out):
  if NaNError not in enabled_errors:
    return error

  def isnan(x):
    if dtypes.issubdtype(x.dtype, dtypes.prng_key):
      return False
    return jnp.any(jnp.isnan(x))

  any_nans = (jnp.any(jnp.array([isnan(x) for x in out]))
              if prim.multiple_results else isnan(out))
  return assert_func(error, any_nans, NaNError(get_traceback(), prim.name))

