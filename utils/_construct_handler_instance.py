
def _construct_handler_instance(
    name: str | None,
    handler_type: Type[CheckpointableHandler],
) -> CheckpointableHandler:
  """Attempts to default-construct a handler type if possible."""
  assert isinstance(handler_type, type)
  try:
    return handler_type()
  except TypeError as e:
    raise ValueError(
        'The :py:class:`~.v1.handlers.CheckpointableHandler`'
        f' resolved for checkpointable={name} could not be default-constructed.'
        ' Please ensure the object is default-constructible or provide a'
        ' concrete instance.'
    ) from e

