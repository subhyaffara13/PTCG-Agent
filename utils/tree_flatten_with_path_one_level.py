from typing import Any

def tree_flatten_with_path_one_level(
    x: Any,
) -> tuple[list[tuple[PyTreePath, Any]], jax.tree_util.PyTreeDef]:
  return jax.tree_util.tree_flatten_with_path(x, is_leaf=lambda y: y is not x)

