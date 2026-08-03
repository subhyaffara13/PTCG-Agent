import os

def _get_protocol(path: PathLike) -> str:
  """Extract the protocol."""
  path = os.fspath(path)
  if '://' in path:
    return path.split('://', 1)[0] + '://'
  else:
    return ''

