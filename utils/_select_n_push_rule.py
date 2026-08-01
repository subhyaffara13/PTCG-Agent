
def _select_n_push_rule(
    ctx: PushRuleContext,
    *args: pallas_core.BlockSpec,
):
  del ctx
  block_specs = [b for b in args if b is not pallas_core.no_block_spec]
  assert len(block_specs) > 0
  block_spec = block_specs[0]
  if len(block_specs) > 1:
    if any(b is not block_spec for b in block_specs):
      raise NotImplementedError(
          'select_n with multiple differing inputs not supported yet'
      )
  return block_spec

