
def _index_switch_op_lowering_rule(
    ctx: LoweringContext, switch_op: scf.IndexSwitchOp
) -> MlirLoweringRuleResult:
  if not inference_utils.should_have_layout(switch_op):
    return _traverse_op_lowering_rule(ctx, switch_op)

  out_layouts = inference_utils.out_layouts(switch_op)
  new_switch_op = scf.IndexSwitchOp(
      _infer_flat_result_types(switch_op, out_layouts),
      switch_op.arg,
      switch_op.cases,
  )

  results_template: Sequence[_VectorTemplate | None] = []
  for region, new_region in zip(
      switch_op.regions, new_switch_op.regions, strict=True
  ):
    [block] = region.blocks
    new_block = new_region.blocks[0]
    results_template = _move_scf_block_to_block_with_flattened_arguments(
        ctx, block, new_block, scf.YieldOp, []
    )
  return _unflatten_ir_values(new_switch_op.results, results_template)

