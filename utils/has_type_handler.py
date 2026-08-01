
def has_type_handler(ty: Any) -> bool:
  """Returns if there is a handler registered for a given type."""
  return GLOBAL_TYPE_HANDLER_REGISTRY.has(ty)

