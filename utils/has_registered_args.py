
def has_registered_args(
    handler: Union[Type[CheckpointHandler], CheckpointHandler]
) -> bool:
  try:
    get_registered_args_cls(handler)
  except ValueError:
    return False
  return True

