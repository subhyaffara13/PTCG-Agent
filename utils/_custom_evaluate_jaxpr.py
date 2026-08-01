
def _custom_evaluate_jaxpr(
    settings: CustomEvaluateSettings, jaxpr: core.Jaxpr, consts, *args
):
  def read(v: core.Atom) -> Any:
    return v.val if isinstance(v, core.Literal) else env[v]

  def write(v: core.Var, val: Any) -> None:
    env[v] = val

  env: dict[core.Var, Any] = {}
  util.safe_map(write, jaxpr.constvars, consts)
  util.safe_map(write, jaxpr.invars, args)
  lu = core.last_used(jaxpr)
  for eqn in jaxpr.eqns:
    bind_params = eqn.primitive.get_bind_params(eqn.params)

    if eqn.primitive in disallowed_primitives:
      raise NotImplementedError(f'Primitive {eqn.primitive} not supported.')
    if not settings.allow_transpose and eqn.primitive is lax.transpose_p:
      raise ValueError('Transpose not allowed.')
    name_stack = (
        source_info_util.current_name_stack() + eqn.source_info.name_stack
    )
    traceback = eqn.source_info.traceback
    with source_info_util.user_context(
        traceback, name_stack=name_stack
    ), eqn.ctx.manager:
      ans = eqn.primitive.bind(
          *util.safe_map(read, eqn.invars), **bind_params
      )
    if eqn.primitive.multiple_results:
      util.safe_map(write, eqn.outvars, ans)
    else:
      write(eqn.outvars[0], ans)
    core.clean_up_dead_vars(eqn, env, lu)
  return util.safe_map(read, jaxpr.outvars)

