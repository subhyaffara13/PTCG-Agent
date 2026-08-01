
def get_storage_type(path: epath.Path | str) -> str:
  """Returns the storage type of the given path."""
  if isinstance(path, str):
    path = epath.Path(path)


  if gcs_utils.is_gcs_path(path):
    return 'gcs'
  else:
    return 'other'

