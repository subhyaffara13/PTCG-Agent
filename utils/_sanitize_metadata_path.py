
def _sanitize_metadata_path(path: epath.PathLike) -> epath.Path:
  """Sanitizes the path and returns it as an `epath.Path`."""
  path = epath.Path(path)
  if path.exists() and not path.is_dir():
    raise NotADirectoryError(f'Path is not a directory: {path}')
  return path

