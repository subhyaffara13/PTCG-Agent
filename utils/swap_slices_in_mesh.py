
def swap_slices_in_mesh(
    mesh: jax.sharding.Mesh, *, replica_axis_index: int = 0
) -> jax.sharding.Mesh:
  """Reverses the ordering of devices such that slices swap IDs."""
  devices = []
  for slice_id in range(
      multislice.replica_count(mesh, replica_axis_index=replica_axis_index)
  ):
    devices.append(
        multislice.replica_devices(
            mesh, replica_id=slice_id, replica_axis_index=replica_axis_index
        )
    )
  devices.reverse()
  devices = np.stack(devices, axis=replica_axis_index)
  return jax.sharding.Mesh(devices, mesh.axis_names)


def swap_slices_in_mesh(
    mesh: jax.sharding.Mesh, *, replica_axis_index: int = 0
) -> jax.sharding.Mesh:
  """Reverses the ordering of devices such that slices swap IDs."""
  devices = []
  for replica_id in range(
      multislice.replica_count(mesh, replica_axis_index=replica_axis_index)
  ):
    devices.append(
        multislice.replica_devices(
            mesh, replica_id=replica_id, replica_axis_index=replica_axis_index
        )
    )
  devices.reverse()
  devices = np.stack(devices, axis=replica_axis_index)
  return jax.sharding.Mesh(devices, mesh.axis_names)

