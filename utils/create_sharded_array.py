
def create_sharded_array(arr, mesh, mesh_axes):
  """Create sharded jax.Array."""
  if isinstance(arr, (int, float)):
    arr = np.asarray(arr)
  return jax.make_array_from_callback(
      arr.shape,
      jax.sharding.NamedSharding(mesh, mesh_axes),
      lambda idx: np.asarray(arr[idx], dtype=arr.dtype),
  )


def create_sharded_array(
    arr: np.ndarray, sharding: jax.sharding.Sharding
) -> jax.Array:
  sharding = cast(jax.sharding.NamedSharding, sharding)
  if isinstance(arr, (int, float)):
    spec = jax.sharding.PartitionSpec()
  else:
    spec = sharding.spec
  return test_utils.create_sharded_array(arr, sharding.mesh, spec)

