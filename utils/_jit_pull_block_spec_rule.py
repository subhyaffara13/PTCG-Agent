
def _jit_pull_block_spec_rule(
    ctx: PullRuleContext, out_block_specs, *, jaxpr, **kwargs
):
  del kwargs
  jaxpr, consts = jaxpr.jaxpr, jaxpr.consts
  if consts:
    raise NotImplementedError('pjit with consts not supported yet')

  def read_usage_env(_: core.Var):
    return {Usage.REGULAR}

  in_block_specs, _ = _pull_block_transform(
      jaxpr,
      out_block_specs,
      scalar_prefetch_handler=ctx.scalar_prefetch_handler,
      read_usage_env=read_usage_env,
      grid_len=ctx.grid_len,
      strict_mode=ctx.strict_mode,
  )
  return in_block_specs

