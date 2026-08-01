
def _7x_create_device_mesh(
    mesh_shape: Sequence[int], devices: Sequence[Any], **unused_kwargs
) -> np.ndarray | None:
  """Creates device assignment for small 7x topologies.

  The device assignment attempts to minimize the number of hops between
  neighbors by allocating rings of devices, and assigns the core axis
  preferentially due to its higher bandwidth.

  Args:
    mesh_shape: Logical mesh shape used by the model.
    devices: TPU devices.
    **unused_kwargs: ...

  Returns:
    None or reordered devices reshaped as `mesh_shape`.
  """
  if len(devices) % 8 != 0 or len(devices) > 32:
    return None

  physical_mesh_shape = _get_physical_tpu_mesh(devices).shape
  # For the x and y axes, we only support at most 2x2 since we can make one ring
  # along those axes and repeat with other separate rings along the z axis.
  if physical_mesh_shape[0] > 2 or physical_mesh_shape[1] > 2:
    return None

  indices = []
  for i in range(0, len(devices), 8):
    new_indices = [x + i for x in _7X_TRAY_2x2x2_RING_ORDER]
    indices.extend(new_indices)

  device_mesh = np.asarray(devices)
  device_mesh = device_mesh[np.array(indices)]
  device_mesh = device_mesh.reshape(mesh_shape)
  return device_mesh

