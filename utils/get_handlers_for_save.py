from typing import Any

def get_handlers_for_save(
    handler_registry: registration.CheckpointableHandlerRegistry,
    checkpointables: dict[str, Any],
) -> dict[str, handler_types.CheckpointableHandler]:
  """Returns a mapping from checkpointable name to handler."""
  return {
      checkpointable_name: registration.resolve_handler_for_save(
          handler_registry, checkpointable, name=checkpointable_name
      )
      for checkpointable_name, checkpointable in checkpointables.items()
  }

