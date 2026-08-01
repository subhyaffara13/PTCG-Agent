
def _is_remote_path(path: str | PathLike[str]):
  """Check whether a path is remote by examining the prefix."""
  # we need to truncate e.g., gs:// to gs:/ because pathlib.Path collapses //
  return any(str(path).startswith(prefix[:-1])
             for prefix in _REMOTE_URL_PREFIXES)

