
def _svd_dtype_rule(dtype, *, compute_uv, **_):
  real_dtype = lax._complex_basetype(dtype)
  if compute_uv:
    return real_dtype, dtype, dtype
  else:
    return real_dtype,

