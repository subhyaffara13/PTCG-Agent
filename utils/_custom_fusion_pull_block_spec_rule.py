
def _custom_fusion_pull_block_spec_rule(
    ctx : block_spec_lib.PullRuleContext,
    out_block_transforms : tuple[block_spec_lib.BlockIndexTransform, ...],
    *,
    pull_block_spec_rule : CustomPullBlockSpecRuleFn,
    **_,
) -> Sequence[block_spec_lib.BlockIndexTransform]:
  del ctx
  return pull_block_spec_rule(out_block_transforms)

