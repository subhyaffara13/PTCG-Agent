from typing import Any

def _check_field_is_hashable(path: tuple[str, ...], x: Any):
  """Checks if a field is hashable."""
  try:
    hash(x)
  except Exception as e:
    path_name = '/'.join(path)
    raise ValueError(f"Value at '{path_name}' is not hashable: {e}") from e

