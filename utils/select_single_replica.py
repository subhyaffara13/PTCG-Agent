
def select_single_replica(
    arrays: List[jax.Array], global_mesh: jax.sharding.Mesh
) -> List[jax.Array]:
  """Returns arrays sharded over single replica."""
  replica_devices = multislice.local_replica_devices(
      global_mesh, replica_axis_index=0
  )
  single_replica_mesh = jax.sharding.Mesh(
      replica_devices, global_mesh.axis_names[1:]
  )

  def _get_single_replica_sharding(arr: jax.Array):
    sharding = typing.cast(jax.sharding.NamedSharding, arr.sharding)
    return jax.sharding.NamedSharding(
        single_replica_mesh,
        jax.sharding.PartitionSpec(*sharding.spec),  # exclude 'replica' axis
    )

  single_replica_shardings = jax.tree.map(
      _get_single_replica_sharding,
      arrays,
  )

  def _make_single_replica_array(
      arr: jax.Array, single_replica_sharding: jax.sharding.NamedSharding
  ):
    data = [
        arr.addressable_data(idx) for idx in range(len(arr.addressable_shards))
    ]
    return jax.make_array_from_single_device_arrays(
        arr.shape, single_replica_sharding, data
    )

  return jax.tree.map(
      _make_single_replica_array, arrays, single_replica_shardings
  )

