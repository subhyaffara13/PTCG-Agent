
def _v5e_create_device_mesh(
    mesh_shape: Sequence[int], devices: Sequence[Any], **unused_kwargs
) -> np.ndarray | None:
  """Creates rotated pincer device assignment for selected topologies.

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

  if bound_x == bound_y == 2 and bound_z == 1 and len(devices) == 4:
    device_mesh = np.asarray(sequential_devices)
    device_mesh = device_mesh[np.array(_TRAY_2x2_RING_ORDER)]
    device_mesh = device_mesh.reshape(mesh_shape)
    return device_mesh

  if len(devices) == 8:
    device_mesh = np.asarray(sequential_devices)
    if bound_x == bound_y == bound_z == 2:  # v5e 2x2x2
      order = _V5E_TRAY_IOTA_ORDER
    else:
      order = _V5E_TRAY_RING_ORDER
    device_mesh = device_mesh[np.array(order)]
    device_mesh = device_mesh.reshape(mesh_shape)
    return device_mesh

  if bound_x == bound_y == 4 and bound_z == 1 and len(devices) == 16:  # v5e4x4
    # Only uses ring order if the whole mesh is a replica group.
    if max(mesh_shape) == len(devices):
      device_mesh = np.asarray(sequential_devices)
      device_mesh = device_mesh[np.array(_TRAY_4x4_RING_ORDER)]
      device_mesh = device_mesh.reshape(mesh_shape)
      return device_mesh

  return None

