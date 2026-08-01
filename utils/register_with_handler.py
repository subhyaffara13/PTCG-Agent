
def register_with_handler(
    handler_cls: Type[CheckpointHandler],
    for_save: bool = False,
    for_restore: bool = False,
):
  """Registers a :py:class:`CheckpointArgs` subclass with a specific handler.

  This registration is necessary so that when the user passes uses this
  :py:class:`CheckpointArgs` class with :py:class:`.CompositeCheckpointHandler`,
  we can automatically find the correct Handler to use to save this class.

  Note, `for_save` and `for_restore` may both be true, but cannot both be false.

  Args:
    handler_cls: `CheckpointHandler` to be associated with this `CheckpointArg`.
    for_save: indicates whether the `CheckpointArg` is registered as a save
      argument.
    for_restore: indicates whether the `CheckpointArg` is registered as a
      restore argument.

  Returns:
    Decorator.
  """
  if not for_save and not for_restore:
    raise ValueError('`for_save` and `for_restore` cannot both be False.')

  def decorator(
      cls: Type[_CheckpointArgsType],
  ) -> Type[_CheckpointArgsType]:
    if not issubclass(cls, CheckpointArgs):
      raise TypeError(
          f'{cls} must subclass `CheckpointArgs` in order to be registered.'
      )
    if for_save:
      _SAVE_ARG_TO_HANDLER[cls] = handler_cls
    if for_restore:
      _RESTORE_ARG_TO_HANDLER[cls] = handler_cls
    handler_type_registry.register_handler_type(handler_cls)
    return cls

  return decorator

