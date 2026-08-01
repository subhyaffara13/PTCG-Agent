
def _get_and_check_device_assignment(
    shardings: Iterable[ShardingInfo],
    ctx_mesh: Mesh | AbstractMesh,
) -> tuple[xc.Client, tuple[xc.Device, ...] | None, int]:
  first_sharding_info = None
  abstract_mesh = (
      ctx_mesh if not ctx_mesh.empty and isinstance(ctx_mesh, AbstractMesh)
      else None)
  any_concrete_sharding = (
      True if not ctx_mesh.empty and isinstance(ctx_mesh, Mesh) else False)

  for sh, s_type, source_info in shardings:
    if isinstance(sh, UnspecifiedValue):
      continue
    elif isinstance(sh, NamedSharding) and isinstance(sh.mesh, AbstractMesh):
      if (abstract_mesh is not None and not sh.mesh.empty and
          abstract_mesh.size != sh.mesh.size):
        raise ValueError("AbstractMesh should be of the same size across all "
                         f"shardings. Got {abstract_mesh} and {sh.mesh}")
      abstract_mesh = sh.mesh
    else:
      any_concrete_sharding = True
      arr_device_assignment = sh._device_assignment
      if first_sharding_info is None:
        first_sharding_info = (arr_device_assignment, s_type, source_info)
      if ctx_mesh.empty:
        if first_sharding_info[0] != arr_device_assignment:
          raise stages.DeviceAssignmentMismatchError([
              stages.DeviceAssignmentMismatch(*first_sharding_info),
              stages.DeviceAssignmentMismatch(
                  arr_device_assignment, s_type, source_info)])
      elif isinstance(ctx_mesh, AbstractMesh):
        if ctx_mesh.size != len(arr_device_assignment):
          raise stages.DeviceAssignmentMismatchError([
              stages.DeviceAssignmentMismatch(
                  ctx_mesh.size, stages.MismatchType.CONTEXT_DEVICES, None),
              stages.DeviceAssignmentMismatch(
                  arr_device_assignment, s_type, source_info)])
      else:
        if ctx_mesh._flat_devices_tuple != arr_device_assignment:
          raise stages.DeviceAssignmentMismatchError([
              stages.DeviceAssignmentMismatch(
                  ctx_mesh._flat_devices_tuple,
                  stages.MismatchType.CONTEXT_DEVICES, None),
              stages.DeviceAssignmentMismatch(
                  arr_device_assignment, s_type, source_info)])

  device_assignment: tuple[xc.Device, ...]
  if (first_sharding_info is None and not ctx_mesh.empty and
      isinstance(ctx_mesh, Mesh)):
    device_assignment = ctx_mesh._flat_devices_tuple
  elif first_sharding_info is None:
    device_assignment = (get_default_device(),)
  else:
    device_assignment = first_sharding_info[0]  # pyrefly: ignore[bad-assignment]

  backend = xb.get_device_backend(device_assignment[0])

  if (any_concrete_sharding and abstract_mesh is not None and
      len(device_assignment) != abstract_mesh.size):
    raise ValueError(
        f"AbstractMesh size: {abstract_mesh.size} does not match the"
        f" device assignment size: {len(device_assignment)}")

  if any_concrete_sharding or abstract_mesh is None:
    return backend, device_assignment, len(device_assignment)
  else:
    return backend, None, abstract_mesh.size

