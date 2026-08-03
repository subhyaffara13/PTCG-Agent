from typing import Any

def is_jax_internal_node(x: Any) -> bool:
  return not is_leaf_node(x)

