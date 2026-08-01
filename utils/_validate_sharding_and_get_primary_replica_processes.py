
def _validate_sharding_and_get_primary_replica_processes(
    replica_axis_index: int,
    primary_replica_id: int,
    sharding: jax.sharding.Sharding,
) -> Set[int]:
  """Validates sharding for restoration."""
  if not isinstance(sharding, jax.sharding.NamedSharding):
    raise InvalidShardingError(
        'The provided sharding is not a NamedSharding. Please use'
        ' NamedSharding instead.'
    )
  primary_replica_device_ids, primary_replica_pids = (
      multislice.get_primary_replica_ids_and_pids(
          replica_axis_idx=replica_axis_index,
          mesh=sharding.mesh,
          primary_replica_id=primary_replica_id,
      )
  )
  if len(primary_replica_device_ids) == len(jax.devices()):
    raise InvalidShardingError(
        'All devices are in the primary replica. There are no non-primary'
        ' replicas to broadcast to.'
    )

  expected_primary_replica_device_ids = {
      d.id
      for d in jax.devices()
      if multihost.process_index_from_device(d) in primary_replica_pids
  }
  if not primary_replica_device_ids.issubset(
      expected_primary_replica_device_ids
  ):
    raise InvalidShardingError(
        'The provided sharding is not valid. The primary replica has the'
        f' following devices: {primary_replica_device_ids}, which is not a'
        ' subset of the expected devices:'
        f' {expected_primary_replica_device_ids}. for the primary processes:'
        f' {primary_replica_pids}.'
    )

  return primary_replica_pids

