
def global_registry() -> CheckpointableHandlerRegistry:
  """Returns the global registry.

  The global registry serves as the default, singleton storage for all
  handlers registered throughout the application's lifecycle via
  `register_handler`.

  Example:
    Retrieve the global registry to inspect available handlers::

      from orbax.checkpoint.v1 import handlers

      # Fetch the singleton global registry
      registry = handlers.global_registry()

      # Check if a specific handler name is registered globally
      is_registered = registry.has("my_custom_model_handler")

  Returns:
    CheckpointableHandlerRegistry: The global singleton registry instance.
  """
  return _GLOBAL_REGISTRY

