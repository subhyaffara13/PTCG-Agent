
def _normalize_mesh_to_colocated_cpu(
    mesh: jax.sharding.Mesh,
) -> jax.sharding.Mesh:
  devices = tuple(mesh.devices.flat)
  if all(_device_platform(device) == 'cpu' for device in devices):
    return mesh
  cpu_devices = np.vectorize(
      _to_serializable_cpu_device, otypes=[object]
  )(mesh.devices)
  return jax.sharding.Mesh(
      cpu_devices, mesh.axis_names, axis_types=mesh.axis_types
  )

