
def _jax_type(dtype: DType, weak_type: bool) -> JAXType:
  """Return the jax type for a dtype and weak type."""
  if weak_type:
    if dtype == bool:
      return dtype
    if dtype in _custom_float_dtypes:
      return float
    return type(dtype.type(0).item())
  return dtype

