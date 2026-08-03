from typing import Any

def _ensure_index(x: Any) -> int | tuple[int, ...]:
  """Ensure x is either an index or a tuple of indices."""
  x = core.concrete_or_error(None, x, "expected a static index or sequence of indices.")
  try:
    return operator.index(x)
  except TypeError:
    return tuple(map(operator.index, x))

