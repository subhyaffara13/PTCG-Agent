
def replica_devices(
    global_mesh: jax.sharding.Mesh,
    *,
    replica_id: int = 0,
    replica_axis_index: int = 0,
) -> np.ndarray:
  """Returns devices for the replica with the given ID."""
  return np.take(
      global_mesh.devices,
      replica_id,
      axis=replica_axis_index,
  )

