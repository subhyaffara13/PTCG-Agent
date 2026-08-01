
def _async_load_tmem_lowering_rule(
    ctx: lowering.LoweringRuleContext, x_ref, *leaves, tree
):
  assert isinstance(x_ref, tcgen05.TMEMRef)
  x_aval = ctx.avals_in[0]
  assert isinstance(x_aval, state_types.AbstractRef)
  transforms = jax.tree.unflatten(tree, leaves)
  transform_avals = tree.unflatten(
      ctx.avals_in[1 : 1 + tree.num_leaves]
  )
  x_tmem, _, transforms = lowering._handle_transforms(
      ctx, x_aval, x_ref, transform_avals, transforms, handle_transposes=False,
      handle_reshapes=False)
  if transforms:
    raise NotImplementedError(
        f"Unimplemented transforms for TMEM refs. {transforms=}"
    )
  layout_hint = None
  if isinstance(ctx.out_layout_hint, mgpu.TiledLayout):
    layout_hint = ctx.out_layout_hint
  is_signed = mgpu_utils.is_signed(ctx.avals_out[0].dtype)
  return x_tmem.load(layout=layout_hint, is_signed=is_signed)

