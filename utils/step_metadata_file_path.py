
def step_metadata_file_path(path: epath.PathLike) -> epath.Path:
  """The path to step metadata file, `_CHECKPOINT_METADATA`."""
  return _sanitize_metadata_path(path) / _STEP_METADATA_FILENAME

