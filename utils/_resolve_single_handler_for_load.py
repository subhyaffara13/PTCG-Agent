
def _resolve_single_handler_for_load(
    checkpointable_name: str,
    handler_registry: registration.CheckpointableHandlerRegistry,
    abstract_checkpointable: Any,
    metadata_handler_typestr: str | None,
) -> handler_types.CheckpointableHandler:
  """Logic to resolve a checkpointable's loading handler.

  1. registration.resolve_handler_for_load performs handler discovery based on
  abstract_checkpointable type and handler_typestr.
  2. If this fails or if abstract_checkpointable and handler_typestr are not
  available, we try to resolve using the default pytree handler if registered.

  Args:
    checkpointable_name: The checkpointable name to resolve the handler for.
    handler_registry: The handler registry to use for resolution.
    abstract_checkpointable: The abstract checkpointable to load.
    metadata_handler_typestr: The handler typestr from the checkpoint metadata.

  Returns:
    The handler for the checkpointable.

  Raises:
    registration.NoEntryError: If no handler is resolved and
    STATE_CHECKPOINTABLE_KEY name is
    not registered.
  """
  # 1. Resolve the checkpointable's handler using handler discovery.
  try:
    return registration.resolve_handler_for_load(
        handler_registry,
        abstract_checkpointable,
        name=checkpointable_name,
        handler_typestr=metadata_handler_typestr,
    )
  except registration.NoEntryError as e:
    logging.warning(
        "Failed to resolve handler for checkpointable: '%s'. Attempting to"
        " load using pytree handler. Error: %s",
        checkpointable_name,
        e,
    )

  # 2. If no handler is resolved yet, try to resolve using the default
  # pytree handler.
  pytree_handler = registration.get_registered_handler_by_name(
      handler_registry, STATE_CHECKPOINTABLE_KEY
  )
  if not pytree_handler:
    raise registration.NoEntryError(
        f"Could not resolve a handler for '{checkpointable_name}' and no"
        f" '{STATE_CHECKPOINTABLE_KEY}' handler found in {handler_registry})."
        " Please inspect the checkpoint contents via"
        " `loading.checkpointables_metadata`. You may need to provide an"
        " abstract_checkpointable or register a missing handler for this name"
        f" or for '{STATE_CHECKPOINTABLE_KEY}' name which is used as a"
        " fallback."
    )
  return pytree_handler

