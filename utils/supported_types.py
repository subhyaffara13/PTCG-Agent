from typing import Any

def supported_types() -> list[Any]:
  """Returns the default list of supported types."""
  return [ty for ty, _ in _DEFAULT_TYPE_HANDLERS]

