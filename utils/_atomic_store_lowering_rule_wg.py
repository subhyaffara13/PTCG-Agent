
def _atomic_store_lowering_rule_wg(
    ctx: lowering.LoweringRuleContext,
    *args_flat,
    args_tree,
    atomic_type: AtomicOpType,
):
  ref, transforms, value = args_tree.unflatten(args_flat)
  ref_aval, transforms_avals, value_aval = args_tree.unflatten(ctx.avals_in)
  value = lowering._ensure_ir_value(value, value_aval.dtype)
  assert isinstance(ref_aval, state_types.AbstractRef)
  ref, _, remaining_transforms = lowering._handle_transforms(
      ctx, ref_aval, ref, list(transforms_avals), list(transforms)
  )
  if remaining_transforms:
    raise NotImplementedError(
        f"Unsupported transforms for atomic_store: {remaining_transforms}"
    )

  mgpu.dialect.vector_store(value, ref, atomic_type=_atomic_op_type_to_int(atomic_type))
  return ()

