from typing import Any

def update_metadata(a, b: dict[str, Any]):
  if not b:
    return a
  if a is None or a is config_ext.unset:
    val = {}
  else:
    val = a.val.copy()
  val.update(b)
  return XlaMetadata(filter_nones(val))

