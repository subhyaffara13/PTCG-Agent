
def construct_checkpoint_args(
    handler: checkpoint_handler.CheckpointHandler,
    for_save: bool,
    *args,
    **kwargs,
) -> checkpoint_args.CheckpointArgs:
  """Constructs `CheckpointArgs` for save or restore for the handler."""
  for arg in args:
    if isinstance(arg, checkpoint_args.CheckpointArgs):
      return arg
  for arg in kwargs.values():
    if isinstance(arg, checkpoint_args.CheckpointArgs):
      return arg
  jax.monitoring.record_event('/jax/orbax/deprecation/checkpointer_legacy_args')
  save_arg_cls, restore_arg_cls = checkpoint_args.get_registered_args_cls(
      handler
  )
  if for_save:
    return save_arg_cls(*args, **kwargs)
  else:
    return restore_arg_cls(*args, **kwargs)

