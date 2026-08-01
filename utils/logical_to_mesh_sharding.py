
def logical_to_mesh_sharding(
  tree: Any,
  mesh: jax.sharding.Mesh,
  rules: LogicalRules | None = None,
) -> Any:
  """Convert pytrees of logical PartitionSpecs to shardings."""
  return jax.tree_util.tree_map(
      lambda x: jax.sharding.NamedSharding(mesh, x),
      logical_to_mesh(tree, rules),
      is_leaf=lambda x: isinstance(x, jax.sharding.PartitionSpec),
  )

