
def local_registry(
    other_registry: CheckpointableHandlerRegistry | None = None,
    *,
    include_global_registry: bool = True,
) -> CheckpointableHandlerRegistry:
  """Creates a local registry.

  This function builds a new registry by optionally combining the existing
  global registry with a provided custom registry. It is highly useful for
  overriding handlers for a specific checkpointer operation without mutating
  the global state.

  Example:
    Create a registry with custom handlers, potentially including global ones::

      from orbax.checkpoint.v1 import handlers

      class MyHandler(handlers.CheckpointableHandler):
        pass

      # Create a registry and add a handler. By default, it includes
      # globally-registered handlers.
      my_registry = handlers.local_registry()
      my_registry.add(MyHandler)

      # To start with an empty registry, use:
      # my_registry = handlers.local_registry(include_global_registry=False)

  Args:
    other_registry: An optional registry of handlers to include in the returned
      registry.
    include_global_registry: If True, includes globally-registered handlers in
      the returned registry by default.

  Returns:
    A local registry.
  """
  registry = _DefaultCheckpointableHandlerRegistry()
  if include_global_registry:
    registry = add_all(registry, global_registry())
  if other_registry:
    registry = add_all(registry, other_registry)
  return registry

