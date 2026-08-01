
def _async_load_tmem_lowering_rule_wg(
    ctx: lowering.LoweringRuleContext, x_ref: ir.Value, *leaves, tree
):
  assert isinstance(x_ref, ir.Value)
  assert isinstance(x_ref.type, ir.MemRefType)
  x_aval = ctx.avals_in[0]
  assert isinstance(x_aval, state_types.AbstractRef)

  transforms = jax.tree.unflatten(tree, leaves)
  transform_avals = tree.unflatten(
      ctx.avals_in[1 : 1 + tree.num_leaves]
  )
  x_tmem, _, transforms = lowering._handle_transforms(
      ctx,
      x_aval,
      x_ref,
      transform_avals,
      transforms,
      handle_transposes=False,
      handle_reshapes=False,
  )
  if transforms:
    raise NotImplementedError(
        f"Unimplemented transforms for TMEM refs. {transforms=}"
    )
  return mgpu.dialect.async_load_tmem(x_tmem)

