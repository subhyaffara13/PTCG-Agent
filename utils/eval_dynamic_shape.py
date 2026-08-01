
def eval_dynamic_shape(ctx: LoweringRuleContext,
                       shape: core.Shape) -> tuple[int | ir.Value, ...]:
  ctx = ctx.replace(
      primitive="eval_dynamic_shape",
      avals_in=[core.dim_value_aval()] * len(ctx.module_context.shape_poly_state.dim_vars),
      tokens_out=None)

  res = lower_fun(
      partial(core.evaluate_shape, shape, ctx.module_context.shape_poly_state.dim_vars),
      multiple_results=True)(ctx, *ctx.dim_var_values)
  flat_res, _ = ir_tree_registry.flatten(res)
  return tuple(operator.index(d) if core.is_constant_dim(d) else d_ir
               for d, d_ir in zip(shape, flat_res))

