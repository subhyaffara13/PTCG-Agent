
def is_orbax_v1_checkpoint(path: path_types.PathLike) -> bool:
  """Determines if the given path is a Orbax checkpoint.

  Args:
    path: The path to the checkpoint directory.

  Returns:
    True if the path is a V1 Orbax checkpoint, False otherwise.
  """

  ctx = context_lib.get_context()
  path = ctx.file_options.path_class(path)
  try:
    asyncio_utils.run_sync(OrbaxLayout().validate_checkpointables(path))
    return True
  except InvalidLayoutError:
    return False

