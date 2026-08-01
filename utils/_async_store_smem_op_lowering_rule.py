
def _async_store_smem_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.AsyncStoreSmemOp
) -> Sequence[ir.Value]:
  index = ir.IndexType.get()

  [to_store_layout] = inference_utils.in_layouts(op)
  value = _fragmented_array_from_ir(op.valueToStore, to_store_layout)
  layout = layouts_lib.from_layout_attr(to_store_layout)
  if not isinstance(layout, fa.TiledLayout):
    raise NotImplementedError(f"Expected TiledLayout, got {type(layout)}")

  ref = op.destination
  transforms_attr = inference_utils.in_transforms(op)[0]
  swizzle = swizzle_from_transforms_attr(transforms_attr)
  unwrapped_ref = unwrap_transformed_memref(ref, transforms_attr)
  tiling_transform, = memref_transforms_from_transforms_attr(transforms_attr)
  assert isinstance(tiling_transform, lc.TileTransform)

  dialect_barrier = utils.DialectBarrierRef.from_barrier_memref(op.barrier)
  barrier_ref = dialect_barrier.barrier_ref

  cluster_dim = gpu.Dimension(op.cluster_dim.value)  # pyrefly: ignore[missing-attribute]
  cluster_idx = arith.index_cast(index, op.cluster_idx)
  cluster_barrier_ref = barrier_ref.remap_to_cluster(cluster_dim, cluster_idx)

  total_bits = math.prod(value.shape) * utils.bitwidth(value.mlir_dtype)
  if total_bits % (8 * utils.WARPGROUP_SIZE):
    raise NotImplementedError(
        f"Transfer of {total_bits} bits is not divisible by "
        f"{8 * utils.WARPGROUP_SIZE}"
    )
  cluster_barrier_ref.arrive_expect_tx(total_bits // 8 // utils.WARPGROUP_SIZE)

  atomic = None
  if op.atomic_type is not None:
    atomic = str(mgpu.AtomicOpType(op.atomic_type.value))  # pyrefly: ignore[missing-attribute]

  def store_tiled_async(optimized: bool):
    value.store_tiled_async(
        unwrapped_ref,
        barrier_ref,
        cluster_dim=cluster_dim,
        cluster_idx=cluster_idx,
        swizzle=swizzle.value if swizzle != mgpu.SwizzlingMode.kNoSwizzle else None,
        optimized=optimized,
        tiling_rank=len(tiling_transform.tiling),
        atomic=atomic,  # pyrefly: ignore[bad-argument-type]
    )

  optimized = op.optimized.value if op.optimized is not None else None
  # TODO(bchetioui): Clean this up.
  _retry_on_failure(store_tiled_async, optimized)
  return []

