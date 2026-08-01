
def dce_jaxpr_xla_metadata_rule(used_outputs: list[bool], eqn: pe.JaxprEqn
                                ) -> tuple[list[bool], pe.JaxprEqn | None]:
  if not any(used_outputs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None
  dced_jaxpr, used_inputs = pe._cached_closed_call_dce(
      eqn.params['jaxpr'], tuple(used_outputs))
  new_params = dict(eqn.params, jaxpr=dced_jaxpr)
  if not any(used_inputs) and not any(used_outputs) and not dced_jaxpr.effects:
    return used_inputs, None
  else:
    new_invars = [v for v, used in zip(eqn.invars, used_inputs) if used]
    new_effs = core.eqn_effects(dced_jaxpr, new_invars)
    new_eqn = pe.new_jaxpr_eqn(
        new_invars,
        [v for v, used in zip(eqn.outvars, used_outputs) if used],
        eqn.primitive, new_params, new_effs, eqn.source_info, eqn.ctx)
    return used_inputs, new_eqn

