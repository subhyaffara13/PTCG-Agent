
def dce_jaxpr_closed_call_rule(used_outputs: list[bool], eqn: JaxprEqn
                               ) -> tuple[list[bool], JaxprEqn | None]:
  # TODO(mattjj): de-duplicate with above rule?
  if not any(used_outputs) and not has_effects(eqn):
    return [False] * len(eqn.invars), None
  jaxpr_ = eqn.params['call_jaxpr']
  closed_jaxpr, used_inputs = _cached_closed_call_dce(jaxpr_, tuple(used_outputs))
  new_invars = [v for v, used in zip(eqn.invars, used_inputs) if used]
  effects = core.eqn_effects(closed_jaxpr, new_invars)
  new_params = dict(eqn.params, call_jaxpr=closed_jaxpr)
  new_eqn = new_jaxpr_eqn(
      new_invars,
      [v for v, used in zip(eqn.outvars, used_outputs) if used],
      eqn.primitive, new_params, effects, eqn.source_info, eqn.ctx)
  return used_inputs, new_eqn

