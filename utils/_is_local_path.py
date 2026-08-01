
def _is_local_path(path: epath.Path) -> bool:
  """Returns True if the path is on a local filesystem namespace."""
  if gcs_utils.is_gcs_path(path):
    return False
  scheme = urlparse(str(path)).scheme
  return not scheme or len(scheme) <= 1

