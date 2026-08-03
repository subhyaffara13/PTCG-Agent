from typing import Any

def get_type_handler(ty: Any) -> types.TypeHandler:
  """Returns the handler registered for a given type, if available."""
  return GLOBAL_TYPE_HANDLER_REGISTRY.get(ty)

