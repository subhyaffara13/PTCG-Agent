
def root_metadata_file_path(
    path: epath.PathLike, *, legacy: bool = False
) -> epath.Path:
  """The path to root metadata file for a given checkpoint directory."""
  filename = (
      _LEGACY_ROOT_METADATA_FILENAME if legacy else _ROOT_METADATA_FILENAME
  )
  return _sanitize_metadata_path(path) / filename

