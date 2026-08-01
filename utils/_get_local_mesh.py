
def _get_local_mesh(global_mesh: Mesh, process_index: int) -> Mesh:
  if global_mesh.empty:
    return global_mesh
  is_local_device = np.vectorize(
      lambda d: d.process_index == process_index, otypes=[bool])(global_mesh.devices)
  subcube_indices = []
  # We take the smallest slice of each dimension that doesn't skip any local device.
  for axis in range(global_mesh.devices.ndim):
    other_axes = tuple_delete(tuple(range(global_mesh.devices.ndim)), axis)
    # NOTE: This re-reduces over many axes multiple times, so we could definitely
    #       optimize it, but I hope it won't be a bottleneck anytime soon.
    local_slices = is_local_device.any(other_axes, keepdims=False)
    nonzero_indices = np.flatnonzero(local_slices)
    start, end = int(np.min(nonzero_indices)), int(np.max(nonzero_indices))
    subcube_indices.append(slice(start, end + 1))
  subcube_indices_tuple = tuple(subcube_indices)
  # We only end up with all conditions being true if the local devices formed a
  # subcube of the full array. This is because we were biased towards taking a
  # "hull" spanned by the devices, and in case the local devices don't form a
  # subcube that hull will contain non-local devices.
  if not is_local_device[subcube_indices_tuple].all():
    raise ValueError(
        "When passing host local inputs to pjit, devices connected to a single"
        " host must form a contiguous subcube of the global device mesh"
    )
  return Mesh(global_mesh.devices[subcube_indices_tuple], global_mesh.axis_names)

