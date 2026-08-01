
def new_jaxpr_eqn(invars, outvars, primitive, params, effects, source_info=None,
                  ctx=None) -> JaxprEqn:
  source_info = source_info or source_info_util.new_source_info()
  ctx = ctx or current_jaxpr_eqn_context()
  effects = resolve_input_effects(effects, invars)
  if config.enable_checks.value:
    assert all(isinstance(x, (Var, Literal)) for x in  invars)
    assert all(isinstance(v,  Var)           for v in outvars)
  return JaxprEqn(invars, outvars, primitive, params, effects, source_info, ctx)

