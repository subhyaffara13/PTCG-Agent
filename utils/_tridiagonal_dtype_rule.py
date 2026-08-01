
def _tridiagonal_dtype_rule(dtype, **_):
  real_dtype = lax._complex_basetype(dtype)
  return dtype, real_dtype, real_dtype, dtype

