import math


def _copy_gmem_to_smem_lowering(
    ctx: lowering.LoweringRuleContext,
    src,
    dst,
    barrier,
    *flat_transforms,
    src_transforms_treedef,
    dst_transforms_treedef,
    barrier_transforms_treedef,
    collective_axes,
    leader_tracked,
    oob_mode,
):
  flat_src_transforms, flat_dst_transforms, flat_barrier_transforms = (
      util.split_list(
          flat_transforms,
          [
              src_transforms_treedef.num_leaves,
              dst_transforms_treedef.num_leaves,
          ],
      )
  )
  flat_src_transforms_avals, flat_dst_transforms_avals, _ = (
      util.split_list(
          ctx.avals_in[3:],
          [
              src_transforms_treedef.num_leaves,
              dst_transforms_treedef.num_leaves,
          ],
      )
  )
  src_transform_avals = src_transforms_treedef.unflatten(
      flat_src_transforms_avals
  )
  src_ref_aval = ctx.avals_in[0]
  dst_ref_aval = ctx.avals_in[1]
  barrier_ref_aval = ctx.avals_in[2]
  src_transforms = src_transforms_treedef.unflatten(flat_src_transforms)
  dst_transforms = dst_transforms_treedef.unflatten(flat_dst_transforms)
  handle_transposes = (
      ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup
  )
  assert isinstance(src_ref_aval, state_types.AbstractRef)
  assert isinstance(dst_ref_aval, state_types.AbstractRef)
  assert isinstance(barrier_ref_aval, state_types.AbstractRef)

  dst_transform_avals = dst_transforms_treedef.unflatten(
      flat_dst_transforms_avals)
  assert len(dst_transform_avals) == len(dst_transforms)
  dst, dst_ref_aval, dst_transforms = lowering._handle_transforms(
      ctx, dst_ref_aval, dst, dst_transform_avals, dst_transforms,
      handle_transposes=handle_transposes)

  copy_params = {
      **_extract_smem_copy_params(dst_ref_aval, dst_transforms),
      **_extract_gmem_copy_params(ctx, src_transforms, src_transform_avals),
  }
  base_index = _get_barrier_base_index(
      barrier_ref_aval,
      barrier_transforms_treedef.unflatten(flat_barrier_transforms),
  )
  if base_index is not None:
    barrier = barrier[base_index]
  collective = None
  if collective_axes is not None:
    collective = tuple(
        lowering._resolve_cluster_axis(ctx.module_ctx.axis_names, axis)
        for axis in collective_axes
    )

  is_leader_tracked_copy = collective and leader_tracked is not None
  dst_ty = ir.MemRefType(dst.type)
  bits = math.prod(dst_ty.shape) * mgpu.bitwidth(dst_ty.element_type)
  if bits % 8:
    raise ValueError(
        f"Can only transfer integer bytes (shape={dst_ty.shape},"
        f" dtype={dst_ty.element_type})"
    )
  bytes = bits // 8

  if is_leader_tracked_copy:
    # Leader receives the completion messages from both CTAs.
    bytes *= 2
    if len(collective) != 1:
      raise ValueError(
          f"Expected exactly one collective axis, got {collective_axes=}"
      )
    if math.prod(ctx.launch_ctx.cluster_size) != 2:
      raise NotImplementedError(
          "Partitioned loads only supported for clusters of size 2. Got"
          f" cluster size {ctx.launch_ctx.cluster_size}."
      )

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    if bytes % WARPGROUP_SIZE:
      raise NotImplementedError(
          "Only copies transferring a number of bytes divisible by the"
          f" warpgroup size are supported. Got {bytes=} but warpgroup size is"
          f" {WARPGROUP_SIZE}"
      )
    if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warpgroup:
      # We arrive uniformly from each thread in the WG, so we need to divide the
      # number of bytes by the number of threads in the WG.
      # TODO: apaszke - Relax this. We can just select the WG leader and have it
      # arrive with the whole transfer size, while everyone else arrives with 0.
      # But we should continue using this scheme as it's likely to be faster.
      bytes //= WARPGROUP_SIZE
      if ctx.module_ctx.auto_barriers:
        mgpu.warpgroup_barrier()  # Make sure all reads have completed.
      if is_leader_tracked_copy:
        first_block = arith_dialect.cmpi(
            arith_dialect.CmpIPredicate.eq,
            mgpu.utils.cluster_idx(collective[0]),
            mgpu.c(0, ir.IndexType.get()),
        )
        barrier.arrive_expect_tx(bytes, predicate=first_block)
      else:
        barrier.arrive_expect_tx(bytes)
    else:
      # In Warp-level lowering, we arrive on each CUDA thread in a warp, but
      # the barrier still expects a full 128 arrivals so we arrive 4 times
      # on each CUDA thread instead.
      # TODO(justinfu): The arrival counts are wrong if called outside of a
      # single warp. Figure out how to guard against this in user code.
      bytes = bytes // WARP_SIZE
      if is_leader_tracked_copy:
        first_block = arith_dialect.cmpi(
            arith_dialect.CmpIPredicate.eq,
            mgpu.utils.cluster_idx(collective[0]),
            mgpu.c(0, ir.IndexType.get()),
        )
        with mgpu.when(first_block):
          barrier.arrive(arrival_count=3, can_complete=False)
          barrier.arrive_expect_tx(bytes)
      else:
        barrier.arrive(arrival_count=3, can_complete=False)
        barrier.arrive_expect_tx(bytes)

    # Gathers are a warpgroup-level collective and can't take a predicate.
    predicate_kwarg = dict(predicate=ctx.module_ctx.single_lane_predicate)
    if gmem_slice := copy_params.get("gmem_slice", ()):
      first_idx = gmem_slice[0]
      if isinstance(first_idx, mgpu.FragmentedArray) and first_idx.shape:
        predicate_kwarg = {}
    ctx.launch_ctx.async_copy(
        src_ref=src,
        dst_ref=dst,
        barrier=barrier,
        arrive=False,
        collective=collective,
        leader_tracked=leader_tracked,
        oob_mode=oob_mode,
        **copy_params,
        **predicate_kwarg,  # pyrefly: ignore[bad-argument-type]
    )
    return ()
  i32 = ir.IntegerType.get_signless(32)
  if "gmem_slice" not in copy_params:
    slice_lengths = ir.MemRefType(src.type).shape
    indices = [mgpu.utils.c(0, i32)] * len(slice_lengths)
  else:
    indices, slice_lengths = _split_gmem_slice(copy_params["gmem_slice"])
  assert copy_params.get("swizzle") is None
  assert not copy_params.get("gmem_transform")
  if copy_params.get("gmem_peer_id", None) is not None:
    raise NotImplementedError(
        "GMEM refs with peer ids are not supported in warpgroup lowering."
    )
  match leader_tracked:
    case CopyPartition.REPLICATED:
      leader_tracked_attr = mgpu.dialect.CopyReplicatedAttr.get()
    case CopyPartition.PARTITIONED(axis):
      leader_tracked_attr = mgpu.dialect.CopyPartitionedAttr.get(axis)
    case _:
      leader_tracked_attr = None

  barrier_ref = barrier.as_barrier_memref()

  if is_leader_tracked_copy:
    first_block = arith_dialect.cmpi(
        arith_dialect.CmpIPredicate.eq,
        mgpu.utils.cluster_idx(collective[0]),
        mgpu.c(0, ir.IndexType.get()),
    )
    arrive_ctx = mgpu.when(first_block)
  else:
    arrive_ctx = contextlib.nullcontext()
  with arrive_ctx:
    mgpu.dialect.arrive_expect_tx(barrier_ref, bytes)

  mgpu.dialect.async_load(
      src,
      dst,
      barrier_ref,
      indices,
      slice_lengths,
      collective=ir.ArrayAttr.get(
          [ir.IntegerAttr.get(i32, axis) for axis in collective or []]
      ),
      leader_tracked=leader_tracked_attr,
      oob_fill_mode=ir.IntegerAttr.get(i32, oob_mode.value)
  )
  return ()

