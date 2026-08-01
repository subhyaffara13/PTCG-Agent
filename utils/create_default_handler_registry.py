
def create_default_handler_registry(
    **items_to_handlers: CheckpointHandler,
) -> CheckpointHandlerRegistry:
  """Creates a registry given a mapping of item names to handlers."""
  registry = DefaultCheckpointHandlerRegistry()
  for item_name, handler in items_to_handlers.items():
    save_args_cls, restore_args_cls = checkpoint_args.get_registered_args_cls(
        handler
    )
    registry.add(item_name, save_args_cls, handler)
    registry.add(item_name, restore_args_cls, handler)
  return registry

