
def device_coords_to_logical_id(device_coords, axis_sizes, axis_indices):
  if isinstance(device_coords, dict):
    device_coords, non_mesh_axes = _device_id_dict_to_mesh(
        device_coords, axis_sizes, axis_indices
    )
    if non_mesh_axes:
      raise NotImplementedError(non_mesh_axes)
  if not isinstance(device_coords, tuple):
    device_coords = (device_coords,)
  assert len(device_coords) == len(axis_sizes)
  sizes = list(axis_sizes.values())
  ret = 0
  for i in range(len(device_coords)):
    ret += device_coords[i] * math.prod(sizes[i + 1 :])
  return ret

