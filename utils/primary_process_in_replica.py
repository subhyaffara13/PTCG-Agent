
def primary_process_in_replica(
    global_mesh: jax.sharding.Mesh,
    *,
    replica_id: int = 0,
    replica_axis_index: int = 0,
) -> int:
  """Returns an arbitrary process in the requested slice to serve as primary."""
  device_replica = replica_devices(
      global_mesh,
      replica_axis_index=replica_axis_index,
      replica_id=replica_id,
  )
  processes = multihost.unique_processes_from_devices(device_replica)
  return next(iter(processes))

