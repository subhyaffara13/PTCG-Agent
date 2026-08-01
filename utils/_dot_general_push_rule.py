
def _dot_general_push_rule(
    ctx: PushRuleContext,
    lhs_block_spec: pallas_core.BlockSpec | pallas_core.NoBlockSpec,
    rhs_block_spec: pallas_core.BlockSpec | pallas_core.NoBlockSpec,
    *,
    dimension_numbers,
    **_,
) -> pallas_core.BlockSpec:
  raise NotImplementedError('dot_general not supported yet')

