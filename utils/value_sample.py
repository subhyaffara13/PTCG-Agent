from typing import Any

def value_sample(values: Any, limit: int = 8) -> str:
  """Returns a compact sample of values for topology logging."""
  values = tuple(values)
  if len(values) <= limit:
    return str(values)
  return f'{values[:limit]} ... ({len(values)} total)'

