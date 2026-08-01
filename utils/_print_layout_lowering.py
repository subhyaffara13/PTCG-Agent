
def _print_layout_lowering(
    ctx: lowering.LoweringRuleContext,
    x: mgpu.FragmentedArray | tcgen05.TMEMRef | ir.Value,
    fmt: str,
    *transforms_leaves,
    transforms_tree
):
  if transforms_leaves:
    assert isinstance(ctx.avals_in[0], state_types.AbstractRef)
    transform_avals = transforms_tree.unflatten(ctx.avals_in[1:])
    x, _, remaining_transforms = lowering._handle_transforms(  # pyrefly: ignore[bad-specialization]
        ctx, ctx.avals_in[0], x, transform_avals,
        transforms_tree.unflatten(transforms_leaves),
    )
    if remaining_transforms:
      raise NotImplementedError(
          f"Unsupported transforms {remaining_transforms}."
      )
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    print(fmt.format(mgpu.dialect_lowering.pprint_layout(x)))  # pyrefly: ignore[bad-argument-type]
  else:
    assert isinstance(x, ir.Value)
    mgpu.dialect.print_layout(fmt, x)
  return ()

