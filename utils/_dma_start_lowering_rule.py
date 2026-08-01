
def _dma_start_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    tree,
    device_id_type: primitives.DeviceIdType,
    priority: int,
    add: bool,
):
  if add:
    raise NotImplementedError("DMA with add=True is not supported.")
  src_ref, dst_ref, sem, src_sem, device_id = _dma_unflatten(tree, args)
  src_ref_aval, dst_ref_aval, sem_aval, src_sem_aval, device_id_aval = (
      _dma_unflatten(tree, ctx.avals_in)
  )
  if any(r.dtype == jnp.bool_ for r in _dma_tree_leaves(src_ref_aval)):
    raise NotImplementedError("DMAs with bool dtypes are not supported.")
  block_shapes = _dma_unflatten(tree, ctx.block_shapes)
  kernel_type = ctx.lowering_context.kernel_type
  if isinstance(sem_aval.memory_space, pallas_core.CoreMemorySpace):
    dest_mesh = sem_aval.memory_space.mesh
    dest_kernel_type = dest_mesh.core_type
  else:
    dest_mesh = None
    dest_kernel_type = kernel_type
  core_id = None
  subcore_id = None
  if device_id is not None or dest_kernel_type != kernel_type:
    with ctx.lowering_context.grid_name_context():
      device_id, core_id, subcore_id = _device_id_to_logical(
          ctx, device_id, device_id_type, device_id_aval, dest_mesh=dest_mesh
      )

  def _dma_start(src_ref, dst_ref, sem, src_sem) -> list[ir.Value]:
    if jaxlib_extension_version < 462:
      assert subcore_id is None, (
          "`subcore_id` is not supported in this version of jaxlib."
      )
      tpu.enqueue_dma(
          source=src_ref,
          target=dst_ref,
          target_semaphore=sem,
          source_semaphore=src_sem,
          device_id=device_id,
          core_id=core_id,
          priority=priority,
      )
    else:
      tpu.enqueue_dma(
          source=src_ref,
          target=dst_ref,
          target_semaphore=sem,
          source_semaphore=src_sem,
          device_id=device_id,
          core_id=core_id,
          subcore_id=subcore_id,  # pyrefly: ignore[unexpected-keyword]
          priority=priority,
      )
    return []

  return lower_with_transformed_refs(
      _dma_start,
      [src_ref, dst_ref, sem, src_sem],
      [src_ref_aval, dst_ref_aval, sem_aval, src_sem_aval],
      block_shapes[:4],)


def _dma_start_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    tree,
    device_id_type: pallas_primitives.DeviceIdType,
    priority: int,
    add: bool,
):
  src_ref, dst_ref, sem, src_sem, device_id = _dma_unflatten(
      tree, args
  )
  src_aval, dst_aval, sem_aval, src_sem_aval, device_id_aval = _dma_unflatten(
      tree, ctx.avals_in
  )

  src_ref, dst_ref, indirect_offsets = _prepare_dma_refs(
      src_ref,
      dst_ref,
      src_aval,
      dst_aval,
      ctx.lowering_context.kernel_type,
      add,
  )
  if add and indirect_offsets is None:
    # TODO: Support regular DMA with add=True.
    raise NotImplementedError(
        "DMAs with `add=True` must (for now) specify offsets of the majormost "
        "dimension. You can do this by writing "
        "`pltpu.async_copy(..., dst_ref=ref.at[jnp.arange(vec_dim)], ...)` or "
        "`pltpu.async_copy(..., dst_ref=ref.at[iota_ref], ...)`."
    )
  core_index = None
  subcore_index = None
  if device_id is not None:
    if isinstance(sem_aval.memory_space, pallas_core.CoreMemorySpace):
      dest_mesh = sem_aval.memory_space.mesh
    else:
      dest_mesh = None
    device_id, core_index, subcore_index = tc_lowering._device_id_to_logical(
        ctx, device_id, device_id_type, device_id_aval, dest_mesh
    )

  # If not ``None``, we lower to an indirect DMA instead.
  if indirect_offsets is None:
    def _dma_start(src_ref, dst_ref, sem, src_sem):
      if jaxlib_extension_version < 462:
        assert subcore_index is None, (
            "`subcore_index` is not supported in this version of jaxlib."
        )
        tpu.enqueue_dma(
            source=src_ref,
            target=dst_ref,
            target_semaphore=sem,
            source_semaphore=src_sem,
            device_id=device_id,
            priority=priority,
            core_id=core_index,
        )
      else:
        tpu.enqueue_dma(
            source=src_ref,
            target=dst_ref,
            target_semaphore=sem,
            source_semaphore=src_sem,
            device_id=device_id,
            priority=priority,
            core_id=core_index,
            subcore_id=subcore_index,  # pyrefly: ignore[unexpected-keyword]
        )
      return []

    return tc_lowering.lower_with_transformed_refs(
        _dma_start,
        [src_ref, dst_ref, sem, src_sem],
        [src_aval, dst_aval, sem_aval, src_sem_aval],
    )

  if device_id is not None:
    raise NotImplementedError(
        "Scatter/gather to or from a remote device via `pltpu.async_copy` is"
        " not supported"
    )

  offset_filter = None
  if indirect_offsets.ignored_value is not None:
    offset_filter = tc_lowering._ensure_mlir_value(
        indirect_offsets.ignored_value, jax_core.ShapedArray((), jnp.int32)
    )

  sem_aval, _ = _get_ref_and_transforms(sem_aval)
  sem, _ = _transform_ref(sem, sem_aval, sem_aval.shape)
  tpu.enqueue_indirect_dma(
      src_ref,
      dst_ref,
      indirect_offsets.values,
      sem,
      add=add,
      offset_filter=offset_filter,
  )
  return []

