
def _is_local_filesystem(path: str) -> bool:
  return path.startswith("file://") or "://" not in path

