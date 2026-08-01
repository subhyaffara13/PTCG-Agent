
def dce_jaxpr_call_rule(used_outputs: list[bool], eqn: JaxprEqn
                        ) -> tuple[list[bool], JaxprEqn | None]:
  if not any(used_outputs) and not has_effects(eqn):
    return [False] * len(eqn.invars), None
  new_jaxpr, used_inputs = dce_jaxpr(eqn.params['call_jaxpr'], used_outputs)
  new_params = dict(eqn.params, call_jaxpr=new_jaxpr)
  update_params = call_param_updaters.get(eqn.primitive)
  if update_params:
    new_params = update_params(new_params, used_inputs, 0)
  if not any(used_inputs) and not any(used_outputs) and not new_jaxpr.effects:
    return used_inputs, None
  else:
    new_invars = [v for v, used in zip(eqn.invars, used_inputs) if used]
    new_eqn = new_jaxpr_eqn(
        new_invars,
        [v for v, used in zip(eqn.outvars, used_outputs) if used],
        eqn.primitive, new_params, core.eqn_effects(new_jaxpr, new_invars),
        eqn.source_info, eqn.ctx)
    return used_inputs, new_eqn

