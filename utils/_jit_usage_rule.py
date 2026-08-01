
def _jit_usage_rule(
    ctx, used_out: list[set[Usage]], *, jaxpr: core.ClosedJaxpr, **_
):
  del ctx
  read_usage_env = compute_usage(jaxpr.jaxpr, used_out)
  in_usages = util.safe_map(read_usage_env, jaxpr.jaxpr.invars)
  return in_usages

