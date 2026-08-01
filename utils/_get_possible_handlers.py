
def _get_possible_handlers(
    registry: CheckpointableHandlerRegistry,
    is_handleable: Callable[[CheckpointableHandler, Any], bool],
    checkpointable: Any | None,
) -> Sequence[CheckpointableHandler]:
  """Raises a NoEntryError if no possible handlers are found."""
  registry_entries = [
      (
          _construct_handler_instance(checkpointable_name, handler),
          checkpointable_name,
      )
      for handler, checkpointable_name in registry.get_all_entries()
  ]
  if checkpointable is None:
    # All handlers are potentially usable if checkpointable is not provided.
    possible_handlers = [
        handler
        for handler, checkpointable_name in registry_entries
        if checkpointable_name is None
    ]
  else:
    possible_handlers = [
        handler
        for handler, checkpointable_name in registry_entries
        if checkpointable_name is None
        and is_handleable(handler, checkpointable)
    ]
  return possible_handlers

