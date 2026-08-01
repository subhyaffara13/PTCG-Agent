
def _custom_fusion_push_block_spec_rule(
    ctx : block_spec_lib.PushRuleContext,
    *block_specs : pallas_core.BlockSpec,
    push_block_spec_rule : CustomPushBlockSpecRuleFn,
    **_
) -> tuple[pallas_core.BlockSpec, ...]:
  del ctx
  # TODO(jburnim): Better error message if push_block_spec_rule is None.
  return push_block_spec_rule(block_specs)

