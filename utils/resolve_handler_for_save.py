from typing import Any

def resolve_handler_for_save(
    registry: CheckpointableHandlerRegistry,
    checkpointable: Any,
    *,
    name: str,
) -> CheckpointableHandler:
  """Resolves a :py:class:`~.v1.handlers.CheckpointableHandler` for saving.

    1. If the checkpointable is a StatefulCheckpointable, prefer to use a
       handler that supports it (e.g. StatefulCheckpointableHandler), bypassing
       explicit name registration.
    2. If a name matching the provided checkpointable name is explicitly
       registered, return the corresponding handler.
    3. Resolve based on the `checkpointable` (using
      :py:meth:`~.v1._src.handlers.types.CheckpointableHandler.is_handleable`).
    4. If multiple handlers are usable, return the *last* usable handler. This
       allows us to resolve the most recently-registered handler.

  Args:
    registry: The
      :py:class:`~.v1.handlers.registration.CheckpointableHandlerRegistry` to
      search.
    checkpointable: A checkpointable to resolve.
    name: The name of the checkpointable.

  Returns:
    A :py:class:`~.v1.handlers.CheckpointableHandler` instance.

  Raises:
    ValueError: If the checkpointable is None.
    NoEntryError: If no compatible
      :py:class:`~.v1.handlers.CheckpointableHandler` can be found.
  """

  if checkpointable is None:
    raise ValueError('checkpointable must not be None for saving.')

  def is_handleable(handler: CheckpointableHandler, ckpt: Any) -> bool:
    return handler.is_handleable(ckpt)

  possible_handlers = _get_possible_handlers(
      registry, is_handleable, checkpointable
  )
  possible_handler = possible_handlers[-1] if possible_handlers else None

  # 1. If the checkpointable is a StatefulCheckpointable, prefer to use a
  # handler that supports it, bypassing explicit name registration.
  if (
      isinstance(checkpointable, handler_types.StatefulCheckpointable)
      and possible_handler
  ):
    return possible_handler

  # 2. If explicitly registered, use that.
  if registry.has(name):
    return _construct_handler_instance(name, registry.get(name))

  # 3 & 4. Resolve based on the checkpointable and return the last usable.
  if possible_handler:
    return possible_handler

  available_handlers = [
      handler_type for handler_type, _ in registry.get_all_entries()
  ]
  raise NoEntryError(
      f'Could not identify a valid handler for the checkpointable: "{name}"'
      f' and checkpointable type={type(checkpointable)}. Make sure to'
      ' register a `CheckpointableHandler` for the object using'
      ' `register_handler`, or by specifying a local registry'
      ' (`CheckpointablesOptions`). If a handler is already registered,'
      ' ensure that `is_handleable` correctly identifies the object as'
      f' handleable. The available handlers are: {available_handlers}'
  )

