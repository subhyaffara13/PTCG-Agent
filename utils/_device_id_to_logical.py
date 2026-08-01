
def _device_id_to_logical(
    ctx: LoweringRuleContext, device_id,
    device_id_type: primitives.DeviceIdType,
    device_id_aval: Any,
    dest_mesh: pallas_core.Mesh | None = None,
):
  kernel_type = ctx.lowering_context.kernel_type
  if dest_mesh is None:
    dest_kernel_type = kernel_type
    core_axis_names = set(ctx.lowering_context.grid_names or ())
  else:
    dest_kernel_type = dest_mesh.core_type
    core_axis_names = set(dest_mesh.shape.keys())

  if (
      ctx.forward_compatible
      and dest_kernel_type != kernel_type
  ):
    raise NotImplementedError(
        "Cannot export MPMD kernels to a different core type when forward"
        f" compatibility is enabled: {kernel_type} -> {dest_kernel_type}"
    )

  spmd_core_axis_names = set(ctx.lowering_context.grid_names or ())
  mpmd_core_axis_names = core_axis_names - spmd_core_axis_names

  def jax_fn(device_id_val):
    if device_id_val is None:
      logical_device_id, core_axis_indices = None, {}
    else:
      logical_device_id, core_axis_indices = primitives.device_id_to_logical(
          ctx.lowering_context.jax_mesh_context,
          device_id_val,
          device_id_type,
          lambda name: lax.axis_index(name),
      )
    # resolve core axis names
    specified_core_axes = set(core_axis_indices.keys())
    missing_mpmd_axes = mpmd_core_axis_names - specified_core_axes
    if dest_kernel_type != kernel_type and missing_mpmd_axes:
      raise ValueError(
          f"When addressing {dest_kernel_type} from {kernel_type} and"
          f" specifying axes={set(core_axis_indices.keys())} the following axes"
          f" are missing from the mesh: {missing_mpmd_axes}. My own grid names"
          f" are {ctx.lowering_context.grid_names}."
      )
    # Resolve the core_indices for every core axis name.
    core_index_map = {
        core_axis_name: core_axis_indices.pop(core_axis_name, None)
        for core_axis_name in core_axis_names
    }
    if core_axis_indices:
      raise ValueError(f"Unrecognized axes in device_id: {core_axis_indices}")

    # We resolve the axis indices in the code below. We already asserted that
    # the required axis names are present in the current kernel type's mesh.
    subcore_index = None
    if dest_kernel_type == tpu_core.CoreType.SC_VECTOR_SUBCORE:
      if not mpmd_core_axis_names and dest_kernel_type == kernel_type:
        # short circuit for same core semaphores without a core type annotation
        return logical_device_id, None, None
      assert isinstance(dest_mesh, sc_core.VectorSubcoreMesh), (
          f"Unrecognized dest_mesh: {type(dest_mesh)} != VectorSubcoreMesh")
      sc_info = tpu_info.get_tpu_info().sparse_core
      assert isinstance(sc_info, tpu_info.SparseCoreInfo)
      if (core_id := core_index_map[dest_mesh.core_axis_name]) is None:
        core_id = lax.axis_index(dest_mesh.core_axis_name)
      if (subcore_id := core_index_map[dest_mesh.subcore_axis_name]) is None:
        subcore_id = lax.axis_index(dest_mesh.subcore_axis_name)
      if jaxlib_extension_version < 462:
        core_index = sc_info.num_subcores * core_id + subcore_id
      else:
        core_index = core_id
        subcore_index = subcore_id
    elif dest_kernel_type == tpu_core.CoreType.SC_SCALAR_SUBCORE:
      if not mpmd_core_axis_names and dest_kernel_type == kernel_type:
        # short circuit for same core semaphores without a core type annotation
        return logical_device_id, None, None
      assert isinstance(dest_mesh, sc_core.ScalarSubcoreMesh), (
          f"Unrecognized dest_mesh: {type(dest_mesh)} != ScalarSubcoreMesh")
      if (core_id := core_index_map[dest_mesh.axis_name]) is None:
        if kernel_type == tpu_core.CoreType.SC_VECTOR_SUBCORE:
          # TODO(rdyro): Mosaic requires resolving the core axis when the
          # target is the scalar subcore, but the source is not. Remove this
          # branch once fixed. We assert earlier that we have this axis name
          # in our mesh.
          # TODO(rdyro): Consider removing this permissive cross-core
          # unspecified core axis special case.
          core_id = lax.axis_index(dest_mesh.axis_name)
      core_index = core_id
    else:
      assert dest_kernel_type == tpu_core.CoreType.TC, (
          f"Unrecognized destination kernel type: {dest_kernel_type} != TC")
      if len(core_index_map) == 0:
        core_index = None
      elif len(core_index_map) == 1:
        (core_index,) = core_index_map.values()
      else:
        raise ValueError(
            f"Expected zero or one core index, got {core_index_map=}.")
    return logical_device_id, core_index, subcore_index

  return lower_fun(jax_fn, in_avals=(device_id_aval,))(ctx, device_id)


def _device_id_to_logical(
    ctx: LoweringRuleContext, device_id,
    device_id_type: primitives.DeviceIdType,
    device_id_aval: Any):
  def jax_fn(device_id_val):
    logical_device_id, non_mesh_axes = primitives.device_id_to_logical(
        ctx.module_ctx.mesh_info,
        device_id_val,
        device_id_type,
        lax.axis_index
    )
    if non_mesh_axes:
        raise ValueError(f"Unrecognized axes in device_id: {non_mesh_axes}")
    return logical_device_id

  return _lower_fun(jax_fn, in_avals=(device_id_aval,))(ctx, device_id)


def _device_id_to_logical(device_id, device_id_type, axis_sizes, axis_indices):
  if device_id is None:
    return None
  if device_id_type == primitives.DeviceIdType.MESH:
    return device_coords_to_logical_id(device_id, axis_sizes, axis_indices)
  elif device_id_type == primitives.DeviceIdType.LOGICAL:
    return device_id
  else:
    raise ValueError(f"Unsupported device ID type: {device_id_type}")

