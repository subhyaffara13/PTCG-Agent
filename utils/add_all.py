
def add_all(
    registry: CheckpointableHandlerRegistry,
    other_registry: CheckpointableHandlerRegistry,
) -> CheckpointableHandlerRegistry:
  """Adds all entries from `other_registry` to `registry`."""
  for handler, name in other_registry.get_all_entries():
    registry.add(
        handler,
        checkpointable_name=name,
        secondary_typestrs=other_registry.get_secondary_typestrs(
            handler
        ),
    )
  return registry

