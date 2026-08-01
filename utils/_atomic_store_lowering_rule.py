
def _atomic_store_lowering_rule(
    ctx: lowering.LoweringRuleContext,
    *args_flat,
    args_tree,
    atomic_type: AtomicOpType,
):
  ref, transforms, value = args_tree.unflatten(args_flat)
  ref_aval, transforms_avals, value_aval = args_tree.unflatten(ctx.avals_in)
  value = lowering._ensure_fa(value, value_aval.dtype)
  assert isinstance(ref_aval, state_types.AbstractRef)
  ref, _, remaining_transforms = lowering._handle_transforms(
      ctx, ref_aval, ref, list(transforms_avals), list(transforms)
  )
  match remaining_transforms:
    case (
        gpu_core.UnswizzleRef(swizzle),
        gpu_core.UntilingTransform(tiling),
    ):
      if len(tiling) != 2:
        raise NotImplementedError(
            f"Only 2D tiling is supported, got: {tiling}"
        )
      value.store_tiled(
          ref, swizzle=swizzle, tiling_rank=len(tiling),
          atomic=atomic_type.value,  # pyrefly: ignore[bad-argument-type]
      )
    case ():
      value.store_untiled(ref, optimized=False, atomic=atomic_type.value)  # pyrefly: ignore[bad-argument-type]
    case _:
      raise NotImplementedError(
          f"Unsupported transforms for atomic_store: {remaining_transforms}"
      )
  return ()

