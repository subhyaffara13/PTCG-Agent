
def _norm_path(path: str | PathLike[str]) -> Any:
  if _is_remote_path(path):
    return pathlib.Path(path)
  return pathlib.Path(path).expanduser().resolve()

