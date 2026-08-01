
def create_single_replica_restore_args(
    arr: jax.Array,
    mesh: jax.sharding.Mesh,
    pspec: jax.sharding.PartitionSpec,
):
  return type_handlers.SingleReplicaArrayRestoreArgs(
      sharding=jax.sharding.NamedSharding(mesh, pspec),
      global_shape=arr.shape,
      dtype=arr.dtype,
  )

