
def process_replica_id(
    process_index: int,
    global_mesh: jax.sharding.Mesh,
    *,
    replica_axis_index: int = 0,
) -> int:
  """Returns the replica id that the process_index belongs to."""

  for replica_id in range(
      replica_count(global_mesh, replica_axis_index=replica_axis_index)
  ):
    device_slice = replica_devices(
        global_mesh,
        replica_id=replica_id,
        replica_axis_index=replica_axis_index,
    )
    if process_index in multihost.unique_processes_from_devices(device_slice):
      return replica_id
  return -1

