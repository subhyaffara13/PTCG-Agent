
def _get_args_for_key(
    handler: CheckpointHandler, item_name: str
) -> Tuple[Type[CheckpointArgs], Type[CheckpointArgs]]:
  """Returns the (save, restore) args for the given item name."""

  if not isinstance(handler, CompositeCheckpointHandler):
    raise ValueError(
        'Expected handler to be a `CompositeCheckpointHandler`, but got'
        f' {type(handler)}.'
    )

  registry = handler._handler_registry  # pylint: disable=protected-access
  for (registered_item, _), handler in registry.get_all_entries().items():
    if registered_item == item_name:
      return checkpoint_args.get_registered_args_cls(handler)
  raise ValueError(f'Unknown key "{item_name}" in CompositeCheckpointHandler.')

