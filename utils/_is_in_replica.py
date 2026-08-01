
def _is_in_replica(
    mesh: jax.sharding.Mesh, replica_axis_index: int, replica_id: int
) -> bool:
  """Returns whether the current process is in the given replica."""
  return multislice.in_replica(
      multihost.process_index(),
      mesh,
      replica_id=replica_id,
      replica_axis_index=replica_axis_index,
  )

