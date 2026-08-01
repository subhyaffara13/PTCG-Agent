
def _mgpu_async_load_op_lowering_rule(
    ctx: LoweringContext, load_op: mgpu.AsyncLoadOp
) -> Sequence[ir.Value]:
  assert ctx.launch_context is not None
  barrier = utils.DialectBarrierRef.from_barrier_memref(load_op.barrier)

  [transforms_attr] = inference_utils.in_transforms(load_op)
  swizzle = swizzle_from_transforms_attr(transforms_attr)
  transforms = memref_transforms_from_transforms_attr(transforms_attr)

  unwrapped_dst = unwrap_transformed_memref(
      load_op.destination, transforms_attr
  )
  assert isinstance(unwrapped_dst.type, ir.MemRefType)
  if utils.is_memref_transposed(unwrapped_dst.type):
    strides, _ = ir.MemRefType(unwrapped_dst.type).get_strides_and_offset()
    permutation = tuple(
        sorted(range(len(strides)), key=lambda i: strides[i], reverse=True)
    )
    # We undo the tranpose and apply it as a transform.
    unwrapped_dst = utils.memref_transpose(
        unwrapped_dst, permutation
    )
    transforms = (*transforms, lc.TransposeTransform(permutation))

  gmem_slice, predicate = _gmem_slice_and_predicate(ctx, load_op)

  collective = [
      gpu.Dimension(ir.IntegerAttr(axis).value)
      for axis in load_op.collective or []
  ]

  match load_op.leader_tracked:
    case mgpu.CopyReplicatedAttr():
      leader_tracked = lc.CopyPartition.REPLICATED
    case mgpu.CopyPartitionedAttr() as attr:
      leader_tracked = lc.CopyPartition.PARTITIONED(attr.axis)
    case _:
      leader_tracked = None

  # TODO(dasenov): async_copy requires all GMEM strides except the last one
  # to be a multiple of 16 bytes. This restriction could be loosned with
  # strided layouts when they are contiguous in GMEM. In that case, we could do:
  # flatten -> async_copy -> unflatted here, as long as flattened size is a
  # multiple of 16.

  if ctx.auto_barriers and ctx.thread_semantics == utils.ThreadSubset.WARPGROUP:
    utils.warpgroup_barrier()  # Make sure the writes have completed.

  # TODO(dasenov): Add support for the remaining op properties.
  oob_mode = lc.OOBFillMode(ir.IntegerAttr(load_op.oob_fill_mode).value)
  ctx.launch_context.async_copy(
      src_ref=load_op.source,
      dst_ref=unwrapped_dst,
      gmem_slice=gmem_slice,
      barrier=barrier.barrier_ref,
      collective=collective,
      arrive=False,
      swizzle=swizzle,
      gmem_transform=transforms,
      leader_tracked=leader_tracked,
      oob_mode=oob_mode,
      **predicate,  # pyrefly: ignore[bad-argument-type]
  )
  return []

