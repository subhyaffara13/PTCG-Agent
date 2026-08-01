
def _for_op_lowering_rule(
    ctx: LoweringContext, for_op: scf.ForOp
) -> MlirLoweringRuleResult:
  if not inference_utils.should_have_layout(for_op):
    return _traverse_op_lowering_rule(ctx, for_op)
  in_layouts = inference_utils.in_layouts(for_op)
  out_layouts = inference_utils.out_layouts(for_op)
  yield_op = for_op.body.operations[len(for_op.body.operations) - 1]
  yield_layouts = inference_utils.in_layouts(yield_op)
  if in_layouts != out_layouts or in_layouts != yield_layouts:
    raise ValueError("Layout mismatch")

  flat_init_args, args_template = _flatten_ir_values(
      for_op.initArgs, in_layouts
  )
  new_for_op = scf.ForOp(
      for_op.lowerBound,
      for_op.upperBound,
      for_op.step,
      flat_init_args,
  )

  _move_scf_block_to_block_with_flattened_arguments(
      ctx,
      for_op.body,
      new_for_op.body,
      scf.YieldOp,
      args_template,
      new_for_op.induction_variable,
  )

  return _unflatten_ir_values(new_for_op.results, args_template)

