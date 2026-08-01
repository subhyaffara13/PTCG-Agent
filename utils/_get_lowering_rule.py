
def _get_lowering_rule(
    ctx: LoweringRuleContext, ref, *idx, tree,
):
  indexers = tree_util.tree_unflatten(tree, idx)
  indexers_avals = tree_util.tree_unflatten(tree, ctx.avals_in[1:])
  # Call _load_lowering_rule (since it's more general)
  ref_aval, *_ = ctx.avals_in
  args_flat, args_tree = tree_util.tree_flatten((ref, indexers, None, None))
  avals_flat = tree_util.tree_leaves((ref_aval, indexers_avals, None, None))
  ctx = ctx.replace(
      avals_in=avals_flat,
      block_shapes=[ctx.block_shapes[0], *[None] * (len(avals_flat) - 1)],
  )
  return _load_lowering_rule(ctx, *args_flat, args_tree=args_tree)


def _get_lowering_rule(ctx: LoweringRuleContext, ref, *flat_transforms, tree):
  return _load_lowering_rule(ctx, ref, None, *flat_transforms, tree=tree)


def _get_lowering_rule(
    ctx: LoweringRuleContext, x_ref, *leaves, tree, optimized=True
):
  if isinstance(x_ref, tcgen05.TMEMRef):
    raise RuntimeError(
        "Loads from TMEM are asynchronous operations and cannot be performed"
        " using the usual syntax. Please use plgpu.async_load_tmem instead."
    )
  if (
      ctx.avals_out[0].shape
      and ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp
  ):
    raise ValueError("Can only load scalars in warp-level code.")
  if not isinstance(x_ref, ir.Value) and isinstance(x_ref, ir.MemRefType):
    raise TypeError(f"Can only load from references (got {x_ref}).")
  dtype = ctx.avals_out[0].dtype

  transforms = jax.tree.unflatten(tree, leaves)
  transposed = ctx.out_layout_hint and ctx.out_layout_hint in (
      mgpu.WGMMA_TRANSPOSED_LAYOUT,
      mgpu.TCGEN05_TRANSPOSED_LAYOUT,
  )
  transposed = bool(transposed)
  assert isinstance(ctx.avals_in[0], state_types.AbstractRef)
  transform_avals = tree.unflatten(ctx.avals_in[1:])
  x_smem, _, transforms = _handle_transforms(
      ctx, ctx.avals_in[0], x_ref, transform_avals, transforms,
      handle_transposes=not transposed, allow_peer_refs=True
  )
  del x_ref  # Don't use x_ref anymore. Use x_smem instead!

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

  if transposed != (permutation is not None):
    raise ValueError(
        "Either both the ref and the value are transposed or neither is."
    )

  is_signed = mgpu_utils.is_signed(dtype)

  if not ctx.avals_out[0].shape:  # The scalar case is simple.
    val = memref_dialect.load(x_smem, [])
    return mgpu.FragmentedArray.splat(val, shape=(), is_signed=is_signed)

  match transforms:
    case (gpu_core.UntilingTransform(tiling),):
      if len(tiling) != 2:
        raise NotImplementedError(f"Only 2D tiling is supported, got: {tiling}")
      if swizzle is None:
        raise NotImplementedError("Tiling without swizzle is not supported.")
      bw = dtypes.itemsize_bits(ctx.avals_out[0].dtype)
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
      return mgpu.FragmentedArray.load_tiled(
          x_smem,
          is_signed=is_signed,
          swizzle=swizzle,
          layout=ctx.out_layout_hint or mgpu.WGMMA_LAYOUT,
          optimized=optimized,
          tiling_rank=len(tiling),
      )
    case ():
      match ctx.out_layout_hint:
        case mgpu.WGStridedFragLayout(shape=shape, vec_size=vec_size):
          assert permutation is None  # strided/transposed rejected above.
          ref_ty = ir.MemRefType(x_smem.type)
          if shape != tuple(ref_ty.shape):
            raise ValueError(
                f"Unsupported shape {shape}, (expected {tuple(ref_ty.shape)})"
            )
          if swizzle is not None:
            raise NotImplementedError(
                "Unsupported swizzle transform with strided layout"
            )
          return mgpu.FragmentedArray.load_strided(
              x_smem,
              is_signed=is_signed,
              vec_size=vec_size,
          )
        case None:
          assert permutation is None  # strided/transposed rejected above.
          if swizzle is not None:
            raise NotImplementedError(
                "Unsupported swizzle transform with strided layout"
            )
          return mgpu.FragmentedArray.load_strided(x_smem, is_signed=is_signed)
        case _:
          assert isinstance(ctx.out_layout_hint, mgpu.TiledLayout)
          if permutation is not None:
            x_smem = mgpu.memref_transpose(x_smem, permutation)
          return mgpu.FragmentedArray.load_untiled(
              x_smem,
              is_signed=is_signed,
              layout=ctx.out_layout_hint,
              swizzle=swizzle or 16,
              optimized=optimized,
          )
    case _:
      raise NotImplementedError(f"Unsupported transforms: {transforms}")


def _get_lowering_rule(ctx: LoweringRuleContext, ptr, *idx, tree):
  indexers = tree_util.tree_unflatten(tree, idx)
  if not _is_triton_pointer_type(ptr.type):
    assert len(indexers) == 0
    return ptr
  args_flat, args_tree = tree_util.tree_flatten((ptr, indexers, None, None))
  return _masked_load_lowering_rule(
      ctx,
      *args_flat,
      args_tree=args_tree,
      eviction_policy=None,
      cache_modifier=None,
      is_volatile=False,
  )

