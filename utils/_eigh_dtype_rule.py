
def _eigh_dtype_rule(dtype, **_):
  return dtype, lax._complex_basetype(dtype)

