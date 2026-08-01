
def get_registered_args_cls(
    handler: Union[Type[CheckpointHandler], CheckpointHandler]
) -> Tuple[Type[CheckpointArgs], Type[CheckpointArgs]]:
  """Returns the registered CheckpointArgs corresponding to the handler.

  Args:
    handler: `CheckpointHandler` instance or class.

  Returns:
    Tuple of (save, restore) `CheckpointArgs` classes.
  """
  save_args = None
  restore_args = None
  if not inspect.isclass(handler):
    handler = type(handler)
  for arg_cls, handler_cls in _SAVE_ARG_TO_HANDLER.items():
    if handler_cls == handler:
      save_args = arg_cls
      break
  if save_args is None:
    raise ValueError(
        f'Unable to find registered `CheckpointArgs` for save for {handler}.'
    )
  for arg_cls, handler_cls in _RESTORE_ARG_TO_HANDLER.items():
    if handler_cls == handler:
      restore_args = arg_cls
      break
  if restore_args is None:
    raise ValueError(
        f'Unable to find registered `CheckpointArgs` for restore for {handler}.'
    )
  return save_args, restore_args

