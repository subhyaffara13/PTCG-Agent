
def remat_dce(used_outputs: list[bool], eqn: core.JaxprEqn
              ) -> tuple[list[bool], core.JaxprEqn | None]:
  if not any(used_outputs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None
  new_jaxpr, used_inputs = pe.dce_jaxpr(eqn.params['jaxpr'], used_outputs)
  prevent_cse = eqn.params['prevent_cse']
  if isinstance(prevent_cse, tuple):
    prevent_cse = tuple(p for p, u in zip(prevent_cse, used_inputs) if u)
  new_params = dict(eqn.params, jaxpr=new_jaxpr, prevent_cse=prevent_cse)
  if (not any(used_inputs) and not any(used_outputs) and
      _has_effects(new_jaxpr.effects)):
    return used_inputs, None
  else:
    new_invars = [v for v, used in zip(eqn.invars, used_inputs) if used]
    new_eqn = pe.new_jaxpr_eqn(
        new_invars,
        [v for v, used in zip(eqn.outvars, used_outputs) if used],
        eqn.primitive, new_params, core.eqn_effects(new_jaxpr, new_invars),
        eqn.source_info, eqn.ctx)
    return used_inputs, new_eqn

