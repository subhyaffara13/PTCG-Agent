
def _while_op_lowering_rule(
    ctx: LoweringContext, while_op: scf.WhileOp
) -> MlirLoweringRuleResult:
  if not inference_utils.should_have_layout(while_op):
    return _traverse_op_lowering_rule(ctx, while_op)

  before_block = while_op.before.blocks[0]
  after_block = while_op.after.blocks[0]
  condition_op = before_block.operations[len(before_block.operations) - 1]
  yield_op = after_block.operations[len(after_block.operations) - 1]

  in_layouts = (
      inference_utils.in_layouts(while_op)
      if inference_utils.should_have_in_layout(while_op)
      else []
  )
  out_layouts = (
      inference_utils.out_layouts(while_op)
      if inference_utils.should_have_out_layout(while_op)
      else []
  )

  if in_layouts:
    yield_layouts = inference_utils.in_layouts(yield_op)
    if in_layouts != yield_layouts:
      raise ValueError(
          f"Input layouts {in_layouts} do not match yield layouts"
          f" {yield_layouts}"
      )

  if out_layouts:
    condition_layouts = inference_utils.in_layouts(condition_op)
    if out_layouts != condition_layouts:
      raise ValueError(
          f"Output layouts {out_layouts} do not match condition layouts"
          f" {condition_layouts}"
      )

  flat_inits, inits_template = _flatten_ir_values(while_op.inits, in_layouts)
  result_types = _infer_flat_result_types(while_op, out_layouts)
  new_while_op = scf.WhileOp(result_types, flat_inits)

  # Before block
  init_types = [v.type for v in flat_inits]
  new_before_block = new_while_op.before.blocks.append(*init_types)
  results_template = _move_scf_block_to_block_with_flattened_arguments(
      ctx,
      before_block,
      new_before_block,
      scf.ConditionOp,
      inits_template,
  )

  # After block
  new_after_block = new_while_op.after.blocks.append(*result_types)
  _move_scf_block_to_block_with_flattened_arguments(
      ctx,
      after_block,
      new_after_block,
      scf.YieldOp,
      results_template,
  )

  return _unflatten_ir_values(new_while_op.results, results_template)

