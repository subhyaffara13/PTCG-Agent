from typing import Any

def flatten_one_level_with_keys(
    tree: Any,
) -> tuple[Iterable[KeyLeafPair], Hashable]:
  """Flatten the given pytree node by one level, with keys."""
  out = default_registry.flatten_one_level_with_keys(tree)
  if out is None:
    raise ValueError(f"can't tree-flatten type: {type(tree)}")
  else:
    return out

