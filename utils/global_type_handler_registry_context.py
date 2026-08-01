
def global_type_handler_registry_context():
  """Context manager for changing the GLOBAL_TYPE_HANDLER_REGISTRY."""
  original_type_handlers = copy.deepcopy(
      type_handler_registry._DEFAULT_TYPE_HANDLERS
  )
  try:
    yield
  finally:
    for original_type, original_handler in original_type_handlers:
      type_handler_registry.GLOBAL_TYPE_HANDLER_REGISTRY.add(
          original_type, original_handler, override=True
      )

