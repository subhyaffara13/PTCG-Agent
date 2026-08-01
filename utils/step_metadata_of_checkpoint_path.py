
def step_metadata_of_checkpoint_path(
    checkpoint_path: epath.PathLike, name_format: NameFormat[MetadataT]
) -> MetadataT:
  """Returns step.MetadataT of given `checkpoint_path`."""
  checkpoint_path = epath.Path(checkpoint_path)
  all_step_metadata = list(name_format.find_all(checkpoint_path.parent))
  for step_metadata in all_step_metadata:
    if step_metadata.path.name == checkpoint_path.name:
      return step_metadata
  raise ValueError(
      'Failed to resolve step metadata of checkpoint path with'
      f' NameFormat={name_format}, checkpoint path={checkpoint_path}, path'
      f' name({checkpoint_path.name}) did not match with available step names:'
      f' {[step_metadata.path.name for step_metadata in all_step_metadata]}.'
      ' Please check if the given path is really a checkpoint path.'
  )

