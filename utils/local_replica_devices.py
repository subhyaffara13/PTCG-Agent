
def local_replica_devices(
    global_mesh: jax.sharding.Mesh, *, replica_axis_index: int = 0
) -> np.ndarray:
  """Get devices for the replica that the current process is in."""
  for replica_id in range(
      replica_count(global_mesh, replica_axis_index=replica_axis_index)
  ):
    if in_replica(
        multihost.process_index(),
        global_mesh,
        replica_id=replica_id,
        replica_axis_index=replica_axis_index,
    ):
      return replica_devices(
          global_mesh,
          replica_id=replica_id,
          replica_axis_index=replica_axis_index,
      )
  raise ValueError(
      f'process_index {multihost.process_index()} does not exist in provided'
      ' `global_mesh`'
  )

