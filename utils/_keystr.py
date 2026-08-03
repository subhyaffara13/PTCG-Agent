from typing import Any, Tuple

def _keystr(key: Tuple[Any, ...]) -> str:
  return '/'.join(key)

