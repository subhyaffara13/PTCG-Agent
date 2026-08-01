
def get_default_temporary_path_class(
    path: epath.Path,
) -> type[atomicity_types.TemporaryPath]:
  """Returns the default temporary path class for a given checkpoint path."""
  if gcs_utils.is_gcs_path(path):
    return atomicity.CommitFileTemporaryPath
  else:
    return atomicity.AtomicRenameTemporaryPath

