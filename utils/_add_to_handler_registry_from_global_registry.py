import logging

def _add_to_handler_registry_from_global_registry(
    registry: handler_registration.CheckpointHandlerRegistry,
    registered_handler_for_args: CheckpointHandler,
    item_name: str,
) -> None:
  """Adds items and handlers to a registry from the global registry."""

  save_args, restore_args = checkpoint_args.get_registered_args_cls(
      registered_handler_for_args
  )

  logging.info(
      'Deferred registration for item: "%s". Adding handler `%s` for item "%s"'
      ' and save args `%s` and restore args `%s` to `_handler_registry`.',
      item_name,
      registered_handler_for_args,
      item_name,
      save_args,
      restore_args,
  )
  registry.add(item_name, save_args, registered_handler_for_args)

  # If the restore args are different from the save args, add them to the
  # registry as well.
  if restore_args != save_args:
    registry.add(item_name, restore_args, registered_handler_for_args)

