
def _custom_fusion_usage_rule(
    ctx : block_spec_lib.UsageRuleContext,
    used_out: Sequence[set[block_spec_lib.Usage]],
    *,
    jaxpr: core.Jaxpr,
    **_
) -> Sequence[set[block_spec_lib.Usage]]:
  del ctx
  # TODO(jburnim): Error if jaxpr.jaxpr gives different usage than pallas_jaxpr?
  read_usage_env = block_spec_lib.compute_usage(jaxpr, used_out)
  return util.safe_map(read_usage_env, jaxpr.invars)

