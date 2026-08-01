
def get_step_metadata(path: epath.PathLike) -> StepMetadata:
  """Returns StepMetadata for a given checkpoint directory."""
  metadata_file_path = checkpoint.step_metadata_file_path(path)
  serialized_metadata = checkpoint.metadata_store(enable_write=False).read(
      metadata_file_path
  )
  if serialized_metadata is None:
    raise ValueError(f'Step metadata not found at {metadata_file_path}')
  return deserialize(serialized_metadata)

