
def _custom_jvp_call_usage_rule(
    ctx, used_out: list[set[Usage]], *, call_jaxpr: core.ClosedJaxpr, **_
):
  del ctx
  read_usage_env = compute_usage(call_jaxpr.jaxpr, used_out)
  in_usages = util.safe_map(read_usage_env, call_jaxpr.jaxpr.invars)
  return in_usages

