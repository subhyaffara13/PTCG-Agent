
def _maybe_implicit_cast(dtype, value):
  aval = core.typeof(value)
  if not isinstance(aval, core.ShapedArray):
    return value
  if (aval.weak_type and
      (dtypes.issubdtype(dtype, np.floating) and
       dtypes.issubdtype(aval.dtype, np.floating)) or
      (dtypes.issubdtype(dtype, np.integer) and
       dtypes.issubdtype(aval.dtype, np.integer))):
    return lax.convert_element_type(value, dtype)
  return value

