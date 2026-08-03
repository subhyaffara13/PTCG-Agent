import os

def _get_first_part(path: str) -> str:
  parts = path.split(os.sep, 1)
  return parts[0]

