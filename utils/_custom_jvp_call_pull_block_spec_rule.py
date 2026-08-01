
def _custom_jvp_call_pull_block_spec_rule(
    ctx: PullRuleContext, out_block_specs, *, call_jaxpr, **kwargs
):
  del kwargs
  jaxpr, consts = call_jaxpr.jaxpr, call_jaxpr.consts
  if consts:
    raise NotImplementedError('custom_jvp_call with consts not supported yet')

  def read_usage_env(_: core.Var):
    return {Usage.REGULAR}

  in_block_specs, _ = _pull_block_transform(
      jaxpr,
      out_block_specs,
      scalar_prefetch_handler=ctx.scalar_prefetch_handler,
      grid_len=ctx.grid_len,
      read_usage_env=read_usage_env,
      strict_mode=ctx.strict_mode,
  )
  return in_block_specs

