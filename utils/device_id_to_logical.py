
def device_id_to_logical(
    mesh_context: pallas_utils.MeshInfo | None,
    device_id: Any,
    device_id_type: DeviceIdType,
    get_axis_index: Callable[[Any], Any],
) -> tuple[Any | None, dict[Any, Any]]:
  """Normalizes a device id into a logical device id and axes that don't correspond to JAX mesh axes.

  The indexing implied by the returned axis dict should be handled by the
  caller. If there are no cross-device operations, then the returned logical
  device id will be None.
  """
  non_mesh_axes = {}
  if isinstance(device_id, dict):
    if device_id_type is not DeviceIdType.MESH:
      raise ValueError(
          "`device_id_type` must be MESH if `device_id` is a dict,"
          f" got: {device_id_type = }."
      )
    device_id, non_mesh_axes = _device_id_dict_to_mesh(mesh_context, device_id, get_axis_index)
  if device_id_type is DeviceIdType.MESH:
    # Mesh means we are passed the mesh coordinates for the device
    device_ids = tree_util.tree_leaves(device_id)
    mesh_strides: tuple[int, ...]
    if mesh_context is None:
      mesh_strides = ()
    else:
      mesh_strides = mesh_context.mesh_strides
    if len(device_ids) != len(mesh_strides):
      raise ValueError(
          "Number of device ids must match the number of mesh axes, but got"
          f" {len(device_ids)} ids for a {len(mesh_strides)}D mesh."
      )

    if not device_ids:
      # If there are no device ids, then it is purely local communication.
      return None, non_mesh_axes
    return sum(a * b for a, b in zip(device_ids, mesh_strides)), non_mesh_axes
  elif device_id_type is DeviceIdType.LOGICAL:
    return device_id, non_mesh_axes
  raise NotImplementedError(f"Unsupported device id type: {device_id_type}")

