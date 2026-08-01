
def _ensure_index_tuple(x: Any) -> tuple[int, ...]:
  """Convert x to a tuple of indices."""
  x = core.concrete_or_error(None, x, "expected a static index or sequence of indices.")
  try:
    return (operator.index(x),)
  except TypeError:
    return tuple(map(operator.index, x))

