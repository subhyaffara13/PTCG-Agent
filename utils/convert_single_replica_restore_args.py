
def convert_single_replica_restore_args(
    restore_args: jax_array_restore_args.SingleReplicaArrayRestoreArgs,
) -> jax_array_restore_args.SingleReplicaArrayRestoreArgs:
  """Converts SingleReplicaArrayRestoreArgs to use colocated CPU devices."""
  if restore_args.single_replica_sharding is not None:
    cpu_single_replica_sharding = colocated_cpu_sharding(
        restore_args.single_replica_sharding
    )
    assert isinstance(cpu_single_replica_sharding, jax.sharding.NamedSharding)
    restore_args = dataclasses.replace(
        restore_args, single_replica_sharding=cpu_single_replica_sharding
    )
  return cast(
      jax_array_restore_args.SingleReplicaArrayRestoreArgs,
      convert_array_restore_args(restore_args),
  )

