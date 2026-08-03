from typing import Any

def _slice_namespace(d: dict[str, Any], name: str) -> dict[str, Any]:
  """Returns entries of `d` keyed `{name}::{key}`, stripped to `{key}`."""
  prefix = f"{name}::"
  return {k[len(prefix) :]: v for k, v in d.items() if k.startswith(prefix)}

