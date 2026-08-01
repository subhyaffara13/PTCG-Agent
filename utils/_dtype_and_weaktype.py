
def _dtype_and_weaktype(value: Any) -> tuple[DType, bool]:
  """Return a (dtype, weak_type) tuple for the given input."""
  return dtype(value), any(value is typ for typ in _weak_types) or is_weakly_typed(value)

