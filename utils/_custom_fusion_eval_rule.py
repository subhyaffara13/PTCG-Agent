
def _custom_fusion_eval_rule(
    ctx: block_spec_lib.KernelEvalContext,
    *args,
    eval_rule: CustomEvalRuleFn,
    num_consts: int,
    pallas_num_consts: int,
    **_):
  args = args[num_consts + pallas_num_consts:]
  return eval_rule(CustomEvalContext(
      out_block_specs=ctx.out_block_specs,
      out_block_indices=ctx.get_out_block_indices(),
  ), *args)

