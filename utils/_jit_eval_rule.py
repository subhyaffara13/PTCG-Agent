
def _jit_eval_rule(ctx: KernelEvalContext, *args, jaxpr, **kwargs):
  jaxpr, consts = jaxpr.jaxpr, jaxpr.consts
  if consts:
    raise NotImplementedError('pjit with consts not supported yet')
  out_tree = tree_util.tree_structure(tuple(jaxpr.outvars))
  in_tree = tree_util.tree_structure((tuple(jaxpr.invars), {}))

  def read_usage_env(_: core.Var):
    return {Usage.REGULAR}

  _, env = _pull_block_spec(
      jaxpr,
      ctx.out_block_specs,
      scalar_prefetch_handler=ctx.scalar_prefetch_handler,
      read_usage_env=read_usage_env,
      grid_len=ctx.grid_len,
  )
  kernel_fn = make_kernel_function(
      jaxpr,
      (),
      in_tree,
      out_tree,
      read_usage_env,
      ctx.in_block_specs,
      env,
      ctx.scalar_prefetch_handler,
      ctx.grid_len,
  )
  return kernel_fn(ctx.get_program_ids(), ctx.scalar_prefetch, *args)

