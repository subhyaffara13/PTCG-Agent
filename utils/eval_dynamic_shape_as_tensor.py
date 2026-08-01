
def eval_dynamic_shape_as_tensor(ctx: LoweringRuleContext,
                                 shape: core.Shape) -> ir.Value:
  """Evaluates the dynamic shapes as one 1d int32 tensor."""
  [x], _ = ir_tree_registry.flatten(
      shape_tensor(ctx.module_context, eval_dynamic_shape(ctx, shape)))
  return x

