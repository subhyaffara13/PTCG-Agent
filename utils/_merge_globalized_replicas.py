
def _merge_globalized_replicas(
    globalized_tree: tuple[jax.Array, ...],
    global_mesh: jax.sharding.Mesh,
):
  """Merges globalized sharded replicas into a single replica."""
  out_sharding = jax.tree.map(
      lambda x: jax.sharding.NamedSharding(
          global_mesh, jax.sharding.PartitionSpec(*x.sharding.spec[1:])
      ),
      globalized_tree,
  )
  out_subtree = jax.jit(
      lambda tree: jax.tree.map(functools.partial(jnp.sum, axis=0), tree),
      out_shardings=out_sharding,
  )(globalized_tree)
  return out_subtree

