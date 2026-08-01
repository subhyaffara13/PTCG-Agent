
def checkpoint_metadata_file_path(path: path_types.Path) -> path_types.Path:
  """The path to step metadata file for a given checkpoint directory."""
  return path / _CHECKPOINT_METADATA_FILENAME

