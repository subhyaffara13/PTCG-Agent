
def in_replica(
    process_index: int,
    global_mesh: jax.sharding.Mesh,
    *,
    replica_id: int = 0,
    replica_axis_index: int = 0,
) -> bool:
  """Returns if the process belongs to the indicated slice ID."""
  return _process_in_device_replica(
      process_index,
      replica_devices(
          global_mesh,
          replica_id=replica_id,
          replica_axis_index=replica_axis_index,
      ),
  )

