from typing import Any

def replicate_on_mesh(tree: Any) -> Any:
  """Replicates a PyTree of arrays across all devices in the current mesh."""
  mesh = jax.sharding.Mesh(np.asarray(jax.devices()), ('devices',))
  sharding = jax.sharding.NamedSharding(mesh, jax.sharding.PartitionSpec())
  return jax.tree.map(
      lambda x: jax.device_put(x, sharding)
      if isinstance(x, (jax.Array, np.ndarray))
      else x,
      tree,
  )

