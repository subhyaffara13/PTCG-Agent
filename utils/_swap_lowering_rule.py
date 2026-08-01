
def _swap_lowering_rule(
    ctx: LoweringRuleContext,
    ref,
    val,
    *idx,
    tree
):
  indexers = tree_util.tree_unflatten(tree, idx)
  indexers_avals = tree_util.tree_unflatten(tree, ctx.avals_in[2:])
  # Call _masked_swap_lowering_rule (since it's more general)
  ref_aval, val_aval, *_ = ctx.avals_in
  args_flat, args_tree = tree_util.tree_flatten((ref, indexers, val, None))
  avals_flat = tree_util.tree_leaves(
      (ref_aval, indexers_avals, val_aval, None)
  )
  ctx = ctx.replace(
      avals_in=avals_flat,
      block_shapes=[ctx.block_shapes[0], *[None] * (len(avals_flat) - 1)],
  )
  return _masked_swap_lowering_rule(ctx, *args_flat, args_tree=args_tree)


def _swap_lowering_rule(
    ctx: LoweringRuleContext, ref, val, *flat_transforms, tree
):
  return _store_lowering_rule(
      ctx, ref, val, None, *flat_transforms, tree=tree, add=False
  )


def _swap_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext, ref, x, *args, has_mask, tree, add
):
  if has_mask:
    *flat_transforms, mask = args
  else:
    flat_transforms, mask = list(args), None
  return sc_lowering._store_lowering_rule(
      ctx, ref, x, mask, *flat_transforms, tree=tree, add=add
  )


def _swap_lowering_rule(
    ctx: LoweringRuleContext, x_ref, value, *leaves, tree
):
  if isinstance(x_ref, tcgen05.TMEMRef):
    raise RuntimeError(
        "Stores to TMEM are asynchronous operations and cannot be performed"
        " using the usual syntax. Please use plgpu.async_store_tmem instead."
    )
  barrier = mgpu.warpgroup_barrier
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if ctx.avals_out[0].shape:
      raise NotImplementedError("Can only store scalars in warp-level lowering.")
    i32 = ir.IntegerType.get_signless(32)
    barrier = functools.partial(
        nvvm_dialect.bar_warp_sync, arith_dialect.constant(i32, -1)
    )
  value = _ensure_fa(value, ctx.avals_in[1].dtype)

  if not isinstance(x_ref, ir.Value) and isinstance(x_ref, ir.MemRefType):
    raise TypeError(f"Can only store to references (got {x_ref}).")
  v_aval = ctx.avals_in[1]
  transforms = jax.tree.unflatten(tree, leaves)
  transposed_value = value.layout in (
      mgpu.WGMMA_TRANSPOSED_LAYOUT,
      mgpu.TCGEN05_TRANSPOSED_LAYOUT,
  )
  transform_avals = jax.tree.unflatten(tree, ctx.avals_in[2:])
  assert isinstance(ctx.avals_in[0], state_types.AbstractRef)
  x_smem, _, transforms = _handle_transforms(
      ctx, ctx.avals_in[0], x_ref, transform_avals, transforms,
      handle_transposes=not transposed_value, allow_peer_refs=True
  )
  del x_ref  # Don't use x_ref anymore. Use x_smem instead!

  if ctx.module_ctx.auto_barriers:
    barrier()  # Make sure reads have completed before we write.

  if transforms and isinstance(transforms[0], gpu_core.UnswizzleRef):
    swizzle = transforms[0].swizzle
    transforms = transforms[1:]
  else:
    swizzle = None

  if transforms and isinstance(transforms[-1], state_types.TransposeTransform):
    permutation = transforms[-1].permutation
    transforms = transforms[:-1]
  else:
    permutation = None

  if transposed_value != (permutation is not None):
    raise ValueError(
        "Either both the ref and the value are transposed or neither is."
    )

  match transforms:
    case _ if math.prod(ctx.avals_out[0].shape) == 1:  # Scalar case.
      zero_idx = _ir_constant(0, ir.IndexType.get())
      indices = [zero_idx] * len(ctx.avals_out[0].shape)
      old_value = mgpu.FragmentedArray.splat(
          memref_dialect.load(x_smem, indices),
          shape=(),
          is_signed=mgpu_utils.is_signed(v_aval.dtype),
      )
      value.store_untiled(x_smem)
    case (gpu_core.UntilingTransform(tiling),):
      if len(tiling) != 2:
        raise NotImplementedError(f"Only 2D tiling is supported, got: {tiling}")
      if swizzle is None:
        raise NotImplementedError("Tiling without swizzle is not supported.")
      bw = dtypes.itemsize_bits(v_aval.dtype)
      expected_minor_tiling = swizzle * 8 // bw
      if tiling[-1] != expected_minor_tiling:
        raise NotImplementedError(
            "Minor tiling dimension does not fit swizzle: "
            f" expected {expected_minor_tiling}, got {tiling[-1]}"
        )

      if permutation is not None:
        if permutation != (1, 0):
          raise NotImplementedError(
              f"Unsupported transpose permutation: {permutation}"
          )
        x_smem = mgpu.memref_transpose(x_smem, (1, 0, 3, 2))

      old_value = mgpu.FragmentedArray.load_tiled(
          x_smem,
          is_signed=mgpu_utils.is_signed(v_aval.dtype),
          swizzle=swizzle,
          layout=value.layout,
          tiling_rank=len(tiling),
      )
      value.store_tiled(x_smem, swizzle=swizzle, tiling_rank=len(tiling))
    case ():
      match value.layout:
        case mgpu.TiledLayout():
          if permutation is not None:
            x_smem = mgpu.memref_transpose(x_smem, permutation)
          old_value = mgpu.FragmentedArray.load_untiled(
              x_smem,
              layout=value.layout,
              is_signed=mgpu_utils.is_signed(v_aval.dtype),
              swizzle=swizzle or 16,
              optimized=False,
          )
          value.store_untiled(x_smem, swizzle=swizzle or 16, optimized=False)
        case _:
          assert permutation is None  # strided/transposed rejected above.
          if swizzle is not None:
            raise NotImplementedError(
                "Unsupported swizzle transform with strided layout"
            )
          old_value = mgpu.FragmentedArray.load_strided(
              x_smem, is_signed=mgpu_utils.is_signed(v_aval.dtype)
          )
          value.store_untiled(x_smem)
    case _:
      raise NotImplementedError(f"Unsupported transforms: {transforms}")
  if ctx.module_ctx.auto_barriers:
    barrier()  # Make sure the writes have completed.
  return old_value


def _swap_lowering_rule(ctx: LoweringRuleContext, ptr, value, *idx, tree):
  indexers = tree_util.tree_unflatten(tree, idx)
  if not _is_triton_pointer_type(ptr.type):
    assert len(indexers) == 0
    return ptr
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  args_flat, args_tree = tree_util.tree_flatten((ptr, indexers, value, None))
  return _masked_swap_lowering_rule(
      ctx, *args_flat, args_tree=args_tree, eviction_policy=None
  )

