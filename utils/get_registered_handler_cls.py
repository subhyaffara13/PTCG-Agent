from typing import Union

def get_registered_handler_cls(
    arg: Union[Type[CheckpointArgs], CheckpointArgs]
) -> Type[CheckpointHandler]:
  """Returns the registered :py:class:`.CheckpointHandler`."""
  if not inspect.isclass(arg):
    arg = type(arg)
  if not issubclass(arg, CheckpointArgs):
    raise TypeError(f'{arg} must be a subclass of `CheckpointArgs`.')
  if arg not in _SAVE_ARG_TO_HANDLER and arg not in _RESTORE_ARG_TO_HANDLER:
    raise ValueError(
        f'Unable to find registered `CheckpointHandler` for {arg}. Use'
        ' `register_with_handler`.'
    )
  if arg in _SAVE_ARG_TO_HANDLER:
    return _SAVE_ARG_TO_HANDLER[arg]
  else:
    return _RESTORE_ARG_TO_HANDLER[arg]

