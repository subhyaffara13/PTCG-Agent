
def _semaphore_signal_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    args_tree,
    device_id_type: primitives.DeviceIdType,
):
  sem_aval, _, _, device_id_aval, _ = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  sem, transforms, value, device_id, core_index = tree_util.tree_unflatten(
      args_tree, args
  )
  sem, _ = _transform_ref(sem, sem_aval, sem_aval.shape, transforms)
  kernel_type = ctx.lowering_context.kernel_type
  if isinstance(sem_aval.memory_space, pallas_core.CoreMemorySpace):
    dest_mesh = sem_aval.memory_space.mesh
    dest_kernel_type = dest_mesh.core_type
  else:
    dest_mesh = None
    dest_kernel_type = kernel_type
  subcore_index = None
  if device_id is not None or dest_kernel_type != kernel_type:
    # TODO(rdyro): Unify the `core_index` argument to use core meshes instead.
    with ctx.lowering_context.grid_name_context():
      device_id, core_id, subcore_index = _device_id_to_logical(
          ctx, device_id, device_id_type, device_id_aval,
          dest_mesh=dest_mesh
      )
    if core_id is not None:
      if core_index is not None:
        raise ValueError(
            "Cannot specify both `core_index` and the core axis in `device_id`."
        )
      core_index = core_id
  if jaxlib_extension_version < 462:
    assert subcore_index is None, (
        "`subcore_index` is not supported in this version of jaxlib."
    )
    tpu.sem_signal(sem, value, device_id=device_id, core_id=core_index)
  else:
    tpu.sem_signal(sem, value, device_id=device_id, core_id=core_index,
                   subcore_id=subcore_index)  # pyrefly: ignore[unexpected-keyword]
  return []


def _semaphore_signal_lowering_rule(
    ctx: lowering.LoweringRuleContext, *args, args_tree,
):
  i32 = ir.IntegerType.get_signless(32)
  sems, transforms, values, device_ids = tree_util.tree_unflatten(
      args_tree, args
  )
  sem_avals, transform_avals, value_avals, device_id_avals = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  transformed_sems = []
  for sem, sem_aval, sem_transform_avals, sem_transforms in zip(
      sems, sem_avals, transform_avals, transforms, strict=True
  ):
    assert isinstance(sem_aval, state_types.AbstractRef)
    sem, _, sem_transforms = lowering._handle_transforms(
        ctx, sem_aval, sem, sem_transform_avals, sem_transforms
    )
    if sem_transforms:
      raise NotImplementedError(f"Unhandled transforms for semaphore_signal_parallel: {sem_transforms}")
    transformed_sems.append(sem)
  del sems, transforms  # Use transformed_sems instead.
  for sem, value, device_id, device_id_aval in zip(
      transformed_sems, values, device_ids, device_id_avals, strict=True
  ):
    if device_id is not None:
      device_id = lowering._device_id_to_logical(
          ctx, device_id, pallas_primitives.DeviceIdType.MESH, device_id_aval
      )
      device_id = lowering._ensure_ir_value(device_id, jnp.int32)
      sem = ctx.launch_ctx.to_remote(sem, device_id)
    val = lowering._ir_constant(value, i32)
    with lowering._wrap_in_custom_primitive_if_wg(ctx, [sem, val]) as [sem, val]:
      sem_ptr = mgpu.utils.memref_ptr(sem)
      # TODO(apaszke): Narrow the scope from .sys to .gpu when the semaphore is local.
      # We only signal the semaphore from a single lane, which does not guarantee
      # anything about the state of the other three warps in the warpgroup (they
      # might still be e.g. reading memory that someone will overwrite once they
      # receive a signal).
      if ctx.module_ctx.auto_barriers:
        mgpu.utils.warpgroup_barrier()
      mgpu_utils.SemaphoreRef(sem_ptr).signal(
          val, predicate=ctx.module_ctx.single_wg_lane_predicate, relaxed=True,
      )
      mgpu_utils.fence_release_sys()
  return ()


def _semaphore_signal_lowering_rule(
    ctx: lowering.LoweringRuleContext,
    *args,
    args_tree,
    device_id_type,
    memory_scope: Literal["sys", "gpu"] = "sys",
):
  i32 = ir.IntegerType.get_signless(32)
  sem, transforms, value, device_id, core_index = tree_util.tree_unflatten(
      args_tree, args
  )
  sem_aval, transform_avals, _, device_id_aval, _ = tree_util.tree_unflatten(
      args_tree, ctx.avals_in
  )
  if core_index is not None:
    raise NotImplementedError(
        "Mosaic GPU backend does not support the concept of cores, but"
        " core_index is specified"
    )
  assert isinstance(sem_aval, state_types.AbstractRef)
  sem, _, transforms = lowering._handle_transforms(
      ctx, sem_aval, sem, transform_avals, transforms
  )
  if transforms:
    raise NotImplementedError(f"Unhandled transforms for semaphore_signal: {transforms}")
  if device_id is not None:
    if memory_scope == "gpu":
      raise ValueError(
          "Cannot signal a GPU-local semaphore from a remote device. Please use"
          " `memory_scope='sys'` instead."
      )
    device_id = lowering._device_id_to_logical(
        ctx, device_id, device_id_type, device_id_aval
    )
    assert device_id is not None
    device_id = lowering._ensure_ir_value(device_id, jnp.int32)
    sem = ctx.launch_ctx.to_remote(sem, device_id)

  val = lowering._ir_constant(value, i32)
  with lowering._wrap_in_custom_primitive_if_wg(ctx, [sem, val]) as [sem, val]:
    sem_ptr = mgpu.utils.memref_ptr(sem)
    # We only signal the semaphore from a single lane, which does not guarantee
    # anything about the state of the other three warps in the warpgroup (they
    # might still be e.g. reading memory that someone will overwrite once they
    # receive a signal).
    if ctx.module_ctx.auto_barriers:
      if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
        mgpu_utils.warp_barrier()
      else:
        mgpu_utils.warpgroup_barrier()

    mgpu_utils.SemaphoreRef(sem_ptr).signal(
        val,
        predicate=ctx.module_ctx.single_lane_predicate,
        memory_scope=memory_scope,
    )
  return ()

