from typing import Any

def is_vmappable(x: Any) -> bool:
  return type(x) in vmappables

