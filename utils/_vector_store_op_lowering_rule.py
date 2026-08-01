
def _vector_store_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.VectorStoreOp
) -> Sequence[ir.Value]:
  if op.atomic_type is not None:
    # pyrefly: ignore[missing-attribute]
    atomic: Any = str(mgpu.AtomicOpType(op.atomic_type.value))
  else:
    atomic = None

  [to_store_layout] = inference_utils.in_layouts(op)
  fragmented_array = _fragmented_array_from_ir(op.valueToStore, to_store_layout)

  if ctx.auto_barriers:
    utils.warpgroup_barrier()  # Make sure the reads have completed.

  ref = op.destination
  ref_type = ir.MemRefType(ref.type)
  optimized = op.optimized.value if op.optimized is not None else None

  if ref_type.memory_space is None:  # GMEM
    ref = utils.MultimemRef(ref) if op.multimem.value else ref
    fragmented_array.store_untiled(
        ref, optimized=bool(optimized), atomic=atomic
    )
  elif ref_type.memory_space == utils.smem():
    transforms_attr = inference_utils.in_transforms(op)[0]
    swizzle = swizzle_from_transforms_attr(transforms_attr)
    transforms = memref_transforms_from_transforms_attr(transforms_attr)
    has_transforms = swizzle != mgpu.SwizzlingMode.kNoSwizzle or transforms
    if has_transforms:
      unwrapped_ref = unwrap_transformed_memref(ref, transforms_attr)
      [tiling_transform] = transforms
      assert isinstance(tiling_transform, lc.TileTransform)

      def store_tiled(optimized: bool):
        fragmented_array.store_tiled(
            unwrapped_ref, swizzle, optimized,
            tiling_rank=len(tiling_transform.tiling),
            atomic=atomic
        )

      _retry_on_failure(store_tiled, optimized)
    else:

      def store_untiled(optimized: bool):
        fragmented_array.store_untiled(ref, optimized=optimized, atomic=atomic)
      _retry_on_failure(store_untiled, optimized)
  else:
    raise ValueError(f"Unsupported memory space: {ref_type.memory_space}")

  if ctx.auto_barriers:
    utils.warpgroup_barrier()  # Make sure the writes have completed.

  return []

