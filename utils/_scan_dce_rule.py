from typing import Any

def _scan_dce_rule(used_outputs: list[bool], eqn: core.JaxprEqn
                   ) -> tuple[list[bool], core.JaxprEqn | None]:
  if not any(used_outputs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None
  jaxpr = eqn.params['jaxpr']
  num_consts, num_carry = eqn.params['num_consts'], eqn.params['num_carry']
  num_xs = len(jaxpr.in_avals) - num_consts - num_carry
  used_carry_out, used_extensive_out = split_list(used_outputs, [num_carry])
  for i in range(1 + num_carry):
    used_outputs = used_carry_out + used_extensive_out
    jaxpr_dce, used_inputs = pe.dce_jaxpr(
        jaxpr.jaxpr, used_outputs,
        instantiate=[False] * num_consts + used_carry_out + [False] * num_xs)
    used_consts, used_carry_in, used_extensive_in = \
        split_list(used_inputs, [num_consts, num_carry])
    if list(used_carry_in) == list(used_carry_out):
      break
    else:
      used_carry_out = _map(operator.or_, used_carry_out, used_carry_in)
  else:
    assert False, "Fixpoint not reached"
  if config.enable_checks.value: core.check_jaxpr(jaxpr.jaxpr)

  new_params = dict[str, Any](
      eqn.params,
      num_consts=sum(used_consts),
      num_carry=sum(used_carry_in),
      jaxpr=ClosedJaxpr(jaxpr_dce, jaxpr.consts)
  )
  # TODO(mattjj,sharadmv): don't assume effects are never DCE'd?
  new_invars = [v for v, used in zip(eqn.invars, used_inputs) if used]
  new_outvars = [v for v, used in zip(eqn.outvars, used_outputs) if used]
  _, new_effects = eqn.primitive.abstract_eval(
      *[v.aval for v in new_invars], **new_params)
  new_eqn = pe.new_jaxpr_eqn(
      new_invars,
      new_outvars,
      eqn.primitive, new_params, new_effects, eqn.source_info, eqn.ctx)
  assert len(new_eqn.invars ) == len(new_params['jaxpr'].in_avals )
  assert len(new_eqn.outvars) == len(new_params['jaxpr'].out_avals)
  return used_inputs, new_eqn

