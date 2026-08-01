
def _create_global_mesh() -> tuple[jax.sharding.Mesh, list[list[jax.Device]]]:
  """Creates a global mesh and returns it along with devices by host and count."""
  devices_by_host = np.asarray(jax.devices()).reshape(
      multihost.process_count(), jax.local_device_count()
  )

  for d in devices_by_host:
    if len(d) != jax.local_device_count():
      raise ValueError("Number of devices must be the same across all hosts.")

  global_mesh = jax.sharding.Mesh(
      np.array(devices_by_host), ("hosts", "devices")
  )
  return global_mesh, devices_by_host

