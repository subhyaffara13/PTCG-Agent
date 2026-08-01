
def _is_float(dtype: _NpDType) -> bool:
  """Validate the dtype is float."""
  # `V` to support bfloat16
  return np.issubdtype(dtype, np.floating) or dtype.kind == 'V'

