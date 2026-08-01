
def _is_valid_base_path(base_path: epath.PathLike) -> bool:
  """Validates base_path and returns it as an epath.Path."""
  base_path = epath.Path(base_path)
  return base_path.exists() and base_path.is_dir()

