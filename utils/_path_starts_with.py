import os

def _path_starts_with(path: str, path_prefix: str) -> bool:
  path = os.path.abspath(path)
  path_prefix = os.path.abspath(path_prefix)
  try:
    common = os.path.commonpath([path, path_prefix])
  except ValueError:
    # path and path_prefix are both absolute, the only case will raise a
    # ValueError is different drives.
    # https://docs.python.org/3/library/os.path.html#os.path.commonpath
    return False
  try:
    return common == path_prefix or os.path.samefile(common, path_prefix)
  except OSError:
    # One of the paths may not exist.
    return False

