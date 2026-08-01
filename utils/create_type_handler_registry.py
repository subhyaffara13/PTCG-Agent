
def create_type_handler_registry(
    *handlers: Tuple[Any, types.TypeHandler]
) -> types.TypeHandlerRegistry:
  """Create a type registry.

  Args:
    *handlers: optional pairs of `(<type>, <handler>)` to initialize the
      registry with.

  Returns:
    A TypeHandlerRegistry instance with only the specified handlers.
  """
  return _TypeHandlerRegistryImpl(*handlers)

