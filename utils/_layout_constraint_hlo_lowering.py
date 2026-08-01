
def _layout_constraint_hlo_lowering(ctx, x_node, *, layout):
  aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  out = mlir.wrap_with_layout_op(ctx, x_node, out_aval, layout, aval)
  return [mlir.lower_with_sharding_in_types(ctx, out, out_aval)]

