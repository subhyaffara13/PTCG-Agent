
def colocated_cpu_devices(
    devices_or_mesh: Sequence[jax.Device],
) -> Sequence[jax.Device]:
  ...


def colocated_cpu_devices(
    devices_or_mesh: jax.sharding.Mesh,
) -> jax.sharding.Mesh:
  ...


def colocated_cpu_devices(devices_or_mesh):
  """Finds devices or a mesh that has CPU devices colocated with the given devices or mesh.

  An accelerator device often accompanies a CPU device that is on the same host.
  Furthermore, when a single host has multiple accelerator devices, there can be
  multiple CPU devices, each of which is associated with one of the accelerator
  devices with a 1:1 correspondence.

  This function finds the colocated CPU devices for the given devices or mesh.
  When the input is a mesh, the returned value is another mesh that has the same
  shape as the input mesh but has colocated CPU devices. If an input device is
  already a CPU device, it is returned as-is.

  It preserves ordering. The output CPU device at index i is associated with the
  input accelerator device at index i.

  Args:
    devices_or_mesh: A tuple of devices or a mesh.

  Returns:
    A tuple of devices or a mesh that has the colocated CPU devices.
  """
  if isinstance(devices_or_mesh, jax.sharding.Mesh):
    return _colocated_cpu_mesh_cached(devices_or_mesh)

  if not isinstance(devices_or_mesh, tuple):
    devices_or_mesh = tuple(devices_or_mesh)
  try:
    return _colocated_cpu_devices_cached(devices_or_mesh)
  except (ValueError, AttributeError):
    return _colocated_cpu_devices_cached_fallback_to_cpu_backend(
        devices_or_mesh
    )

