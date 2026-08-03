from typing import Any

def logical_to_mesh(tree: Any, rules: LogicalRules | None = None) -> Any:
  """Applies logical_to_mesh_axes to pytrees of logical PartitionSpecs."""
  return jax.tree_util.tree_map(
      lambda x: logical_to_mesh_axes(x, rules),
      tree,
      is_leaf=lambda x: isinstance(x, jax.sharding.PartitionSpec),
  )

