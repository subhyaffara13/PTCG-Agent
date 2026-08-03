from typing import Any

def _v5p_create_device_mesh(
    mesh_shape: Sequence[int], devices: Sequence[Any], **unused_kwargs
) -> np.ndarray | None:
  """Creates device assignment for selected topologies.

  Args:
    mesh_shape: Logical mesh shape used by the model.
    devices: TPU devices.
    **unused_kwargs: ...

  Returns:
    None or reordered devices reshaped as `mesh_shape`.
  """
  max_x, max_y, max_z = max(getattr(d, "coords", (0, 0, 0)) for d in devices)
  bound_x, bound_y, bound_z = max_x + 1, max_y + 1, max_z + 1
  # Our ring re-ordering makes sense only if the passed-in devices are
  # sequential, which may not always be the case. reversed() changes z-minor to
  # x-minor.
  sequential_devices = sorted(
      devices,
      key=lambda d: tuple(reversed(getattr(d, "coords", (0, 0, 0)))))

  if bound_x == bound_y == bound_z == 2 and len(devices) == 8:
    device_mesh = np.asarray(sequential_devices)
    device_mesh = device_mesh[np.array(_V5P_2x2x2_ORDER)]
    device_mesh = device_mesh.reshape(mesh_shape)
    return device_mesh
  return None

