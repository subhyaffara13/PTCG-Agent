
def dce_jaxpr_compute_on_rule(used_outputs: list[bool], eqn: pe.JaxprEqn
                              ) -> tuple[list[bool], pe.JaxprEqn | None]:
  if not any(used_outputs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None

  dced_jaxpr, used_inputs = pe._cached_closed_call_dce(
      eqn.params['jaxpr'], tuple(used_outputs))

  def keep_where(xs, keeps):
    return tuple(x for x, keep in zip(xs, keeps) if keep)

  new_params = dict(eqn.params, jaxpr=dced_jaxpr,
                    out_memory_spaces=keep_where(eqn.params["out_memory_spaces"],
                                                 used_outputs))
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

