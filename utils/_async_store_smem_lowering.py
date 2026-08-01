
def _async_store_smem_lowering(
    ctx: lowering.LoweringRuleContext,
    src,
    ref,
    barrier,
    cluster_idx,
    *flat_transforms,
    ref_transforms_treedef,
    barrier_transforms_treedef,
    cluster_dim,
    optimized,
    atomic,
):
  flat_ref_transforms, flat_barrier_transforms = util.split_list(
      flat_transforms,
      [ref_transforms_treedef.num_leaves],
  )
  flat_ref_transforms_avals, _ = util.split_list(
      ctx.avals_in[4:],
      [ref_transforms_treedef.num_leaves],
  )

  ref_transform_avals = ref_transforms_treedef.unflatten(
      flat_ref_transforms_avals
  )
  ref_aval = ctx.avals_in[1]
  barrier_ref_aval = ctx.avals_in[2]
  assert isinstance(ref_aval, state_types.AbstractRef)
  assert isinstance(barrier_ref_aval, state_types.AbstractRef)

  ref_transforms = ref_transforms_treedef.unflatten(flat_ref_transforms)
  barrier_transforms = barrier_transforms_treedef.unflatten(flat_barrier_transforms)

  ref_smem, _, remaining_ref_transforms = lowering._handle_transforms(
      ctx,
      ref_aval,
      ref,
      ref_transform_avals,
      ref_transforms,
      handle_transposes=True,
  )

  base_index = _get_barrier_base_index(barrier_ref_aval, barrier_transforms)
  if base_index is not None:
    barrier = barrier[base_index]

  cluster_idx_val = lowering._as_index(cluster_idx)
  gpu_cluster_dim = lowering._resolve_cluster_axis(ctx.module_ctx.axis_names, cluster_dim)

  shape = ctx.avals_in[0].shape
  dtype = ctx.avals_in[0].dtype
  if not shape:
    raise NotImplementedError("Scalars are not supported in async_store_smem")

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    if remaining_ref_transforms:
      raise ValueError(f"Unexpected unhandled transforms: {remaining_ref_transforms}")
    assert isinstance(barrier, mgpu.DialectBarrierRef)
    cluster_idx_i32 = arith_dialect.index_cast(
        ir.IntegerType.get_signless(32), cluster_idx_val
    )
    atomic_type = None
    if atomic is not None:
      atomic_type = _atomic_op_type_to_int(AtomicOpType(atomic))
    mgpu.dialect.async_store_smem(
        src,
        ref_smem,
        barrier.as_barrier_memref(),
        gpu_cluster_dim.value,
        cluster_idx_i32,
        atomic_type=atomic_type,
        optimized=optimized,
    )
    return ()

  match remaining_ref_transforms:
    case (gpu_core.UnswizzleRef(swizzle), gpu_core.UntilingTransform(tiling)):
      pass
    case _:
      raise NotImplementedError("async_store_smem requires a tiled and swizzled ref")

  total_bits = math.prod(shape) * dtypes.itemsize_bits(dtype)
  if total_bits % 8:
    raise ValueError(
        f"Can only transfer integer bytes (shape={shape}, dtype={dtype})"
    )
  total_bytes = total_bits // 8
  if total_bytes % WARPGROUP_SIZE:
    raise NotImplementedError(f"Transfer is not a multiple of {WARPGROUP_SIZE} bytes")

  peer_barrier = barrier.remap_to_cluster(gpu_cluster_dim, cluster_idx_val)
  peer_barrier.arrive_expect_tx(total_bytes // WARPGROUP_SIZE)

  lowering._ensure_fa(src, dtype).store_tiled_async(
      ref_smem,
      barrier,
      cluster_dim=gpu_cluster_dim,
      cluster_idx=cluster_idx_val,
      swizzle=swizzle,
      optimized=optimized,
      tiling_rank=len(tiling),
      atomic=atomic,
  )
  return ()

