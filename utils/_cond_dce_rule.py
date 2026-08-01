
def _cond_dce_rule(used_outputs: list[bool], eqn: core.JaxprEqn,
                   ) -> tuple[list[bool], core.JaxprEqn | None]:

  if not any(used_outputs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None

  closed_branches = eqn.params['branches']
  branches = [closed_jaxpr.jaxpr for closed_jaxpr in closed_branches]

  # First, compute which inputs are used in any branch (not including `pred`).
  used_inputs: list[bool] = [False] * (len(eqn.invars) - 1)  # -1 for pred
  for jaxpr in branches:
    _, used_inputs_ = pe.dce_jaxpr(jaxpr, used_outputs, instantiate=False)
    used_inputs = map(operator.or_, used_inputs, used_inputs_)

  # Next, compute DCEd branches, instantiating according to used_inputs.
  dce_branches_ = [pe.dce_jaxpr(jaxpr, used_outputs, instantiate=used_inputs)[0]
                   for jaxpr in branches]
  dce_branches = [core.ClosedJaxpr(jaxpr, closed_jaxpr.consts)
                  for closed_jaxpr, jaxpr in zip(closed_branches, dce_branches_)]

  # Finally, update parameters and form the new eqn.
  new_params = dict(eqn.params, branches=tuple(dce_branches))
  new_effects = _join_cond_effects(dce_branches)
  new_eqn = pe.new_jaxpr_eqn(
      [v for v, used in zip(eqn.invars, [True, *used_inputs]) if used],
      [v for v, used in zip(eqn.outvars, used_outputs) if used],
      eqn.primitive, new_params, new_effects, eqn.source_info, eqn.ctx)

  assert all(len(new_eqn.invars ) == 1 + len(jaxpr.in_avals )
             for jaxpr in new_params['branches'])
  assert all(len(new_eqn.outvars) == len(jaxpr.out_avals)
             for jaxpr in new_params['branches'])
  return [True, *used_inputs], new_eqn

