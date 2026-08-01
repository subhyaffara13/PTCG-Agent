
def _mgpu_async_store_op_lowering_rule(
    ctx: LoweringContext, store_op: mgpu.AsyncStoreOp
) -> Sequence[ir.Value]:
  assert ctx.launch_context is not None

  [transforms_attr] = inference_utils.in_transforms(store_op)
  swizzle = swizzle_from_transforms_attr(transforms_attr)
  transforms = memref_transforms_from_transforms_attr(transforms_attr)
  unwrapped_source = unwrap_transformed_memref(store_op.source, transforms_attr)
  assert isinstance(unwrapped_source.type, ir.MemRefType)
  if utils.is_memref_transposed(unwrapped_source.type):
    strides, _ = ir.MemRefType(unwrapped_source.type).get_strides_and_offset()
    permutation = tuple(
        sorted(range(len(strides)), key=lambda i: strides[i], reverse=True)
    )
    # We undo the tranpose and apply it as a transform.
    unwrapped_source = utils.memref_transpose(
        unwrapped_source, permutation
    )
    transforms = (*transforms, lc.TransposeTransform(permutation))

  gmem_slice, predicate = _gmem_slice_and_predicate(ctx, store_op)

  arrive = (
      None if store_op.commit_group is None else bool(store_op.commit_group)
  )

  # TODO(dasenov): async_copy requires all GMEM strides except the last one
  # to be a multiple of 16 bytes. This restriction could be loosned with
  # strided layouts when they are contiguous in GMEM. In that case, we could do:
  # flatten -> async_copy -> unflatted here, as long as flattened size is a
  # multiple of 16.
  if store_op.reduction_op is not None:
    # pyrefly: ignore[missing-attribute]
    reduction_op = mgpu.TMAReduction(store_op.reduction_op.value).name.lower()
  else:
    reduction_op = None

  peer_id: ir.Value | lc.GlobalBroadcast | None = None
  if store_op.is_global_broadcast.value:
    peer_id = lc.GLOBAL_BROADCAST
  elif store_op.gmem_peer_id is not None:
    peer_id = store_op.gmem_peer_id

  # TODO(dasenov): Add support for the remaining op properties.
  ctx.launch_context.async_copy(
      src_ref=unwrapped_source,
      dst_ref=store_op.destination,
      gmem_slice=gmem_slice,
      swizzle=swizzle,
      gmem_transform=transforms,
      **predicate,  # pyrefly: ignore[bad-argument-type]
      arrive=arrive,
      reduction_op=reduction_op,  # pyrefly: ignore[bad-argument-type]
      gmem_peer_id=peer_id,
      oob_mode=lc.OOBFillMode.UNDEFINED,
  )
  return []

