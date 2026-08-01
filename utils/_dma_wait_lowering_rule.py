
def _dma_wait_lowering_rule(ctx: LoweringRuleContext, *args, tree,
                            device_id_type: primitives.DeviceIdType,
                            insert_dummy_device: bool):
  src, dst, sem, _, device_id = _dma_unflatten(tree, args)
  src_aval, dst_aval, sem_aval, _, device_id_aval = _dma_unflatten(
      tree, ctx.avals_in
  )
  block_shapes = _dma_unflatten(tree, ctx.block_shapes)

  if insert_dummy_device:
    i32 = ir.IntegerType.get_signless(32)
    device_id = core_id = arith.constant(i32, ir.IntegerAttr.get(i32, 0))
  elif device_id is not None:
    if isinstance(sem_aval.memory_space, pallas_core.CoreMemorySpace):
      dest_mesh = sem_aval.memory_space.mesh
    else:
      dest_mesh = None
    device_id, core_id, _ = _device_id_to_logical(
        ctx, device_id, device_id_type, device_id_aval, dest_mesh=dest_mesh
    )
  else:
    core_id = None

  def _dma_wait(src_ref, dst_ref, sem) -> list[ir.Value]:
    tpu.wait_dma2(sem, src_ref, dst_ref, device_id=device_id, core_id=core_id)
    return []

  return lower_with_transformed_refs(_dma_wait, [src, dst, sem], [src_aval, dst_aval, sem_aval], block_shapes[:3])


def _dma_wait_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    tree,
    device_id_type: pallas_primitives.DeviceIdType,
    insert_dummy_device: bool,
):
  src_ref, dst_ref, sem, _, device_id = _dma_unflatten(
      tree, args
  )
  src_aval, dst_aval, sem_aval, _, device_id_aval = _dma_unflatten(
      tree, ctx.avals_in
  )

  src_ref, dst_ref, indirect_offsets = _prepare_dma_refs(
      src_ref,
      dst_ref,
      src_aval,
      dst_aval,
      ctx.lowering_context.kernel_type,
  )
  core_id = None
  subcore_id = None
  if insert_dummy_device:
    i32 = ir.IntegerType.get_signless(32)
    core_id = device_id = arith.constant(i32, ir.IntegerAttr.get(i32, 0))
  elif device_id is not None:
    if isinstance(sem_aval.memory_space, pallas_core.CoreMemorySpace):
      dest_mesh = sem_aval.memory_space.mesh
    else:
      dest_mesh = None
    device_id, core_id, subcore_id = tc_lowering._device_id_to_logical(
        ctx, device_id, device_id_type, device_id_aval, dest_mesh
    )
    if core_id:
      raise NotImplementedError(
          "Core index must be None when waiting on a local DMA."
      )
    if subcore_id:
      raise NotImplementedError(
          "Subcore index must be None when waiting on a local DMA."
      )

  # If not ``None``, we lower to an indirect DMA instead of a regular DMA.
  if indirect_offsets is None:
    def _dma_wait(src_ref, dst_ref, sem):
      # `wait_dma2` does not support `subcore_id`, so it is ignored until
      # we migrate to `wait_dma`.
      tpu.wait_dma2(
        sem, src_ref, dst_ref, device_id=device_id, core_id=core_id
      )
      return []
    return tc_lowering.lower_with_transformed_refs(
        _dma_wait,
        [src_ref, dst_ref, sem],
        [src_aval, dst_aval, sem_aval],
    )

  if device_id is not None:
    raise NotImplementedError(
        "Scatter/gather to or from a remote device via `pltpu.async_copy` is"
        " not supported"
    )
  sem_aval, _ = _get_ref_and_transforms(sem_aval)
  sem, _ = _transform_ref(sem, sem_aval, sem_aval.shape)
  tpu.wait_indirect_dma(sem, src_ref, dst_ref)
  return []

