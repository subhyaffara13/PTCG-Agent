
def get_named_sharding(tree: A, mesh: jax.sharding.Mesh) -> A:
  spec = get_partition_spec(tree)
  sharding = jax.tree.map(lambda p: jax.sharding.NamedSharding(mesh, p), spec)
  return sharding

