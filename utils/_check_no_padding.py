from typing import Any

def _check_no_padding(axis_padding: tuple[Any, Any], mode: str):
  if (axis_padding[0] > 0 or axis_padding[1] > 0):
    msg = "Cannot apply '{}' padding to empty axis"
    raise ValueError(msg.format(mode))

