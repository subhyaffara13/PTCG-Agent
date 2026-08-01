
def _custom_jvp_call_dce(
    used_outs: Sequence[bool], eqn: core.JaxprEqn
) -> tuple[list[bool], core.JaxprEqn | None]:
  if not any(used_outs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None

  call_jaxpr = eqn.params["call_jaxpr"]
  jvp_jaxpr_fun = eqn.params["jvp_jaxpr_fun"]
  # We must set instantiate=True because some inputs that are unused by the
  # DCE'ed primal might be used in the JVP rule.
  dce_call_jaxpr, used_ins = _cached_closed_call_dce_instantiate(
      call_jaxpr, tuple(used_outs))
  assert all(used_ins)

  @pe._memoize
  def dce_jvp_jaxpr_thunk(*in_zeros):
    jvp_jaxpr, consts, out_zeros = jvp_jaxpr_fun.call_wrapped(*in_zeros)
    sz = eqn.params["symbolic_zeros"]
    nz_used_outs = [u for u, z in zip(used_outs, out_zeros) if not z] if sz else used_outs
    dce_jvp_jaxpr, _ = pe.dce_jaxpr(jvp_jaxpr, [*used_outs, *nz_used_outs], True)
    dce_out_zeros = [v for used, v in zip(used_outs, out_zeros) if used]
    return dce_jvp_jaxpr, consts, dce_out_zeros

  outvars = [v for used, v in zip(used_outs, eqn.outvars) if used]
  new_params = dict(
      eqn.params,
      call_jaxpr=dce_call_jaxpr,
      jvp_jaxpr_fun=lu.wrap_init(dce_jvp_jaxpr_thunk,
                                 debug_info=jvp_jaxpr_fun.debug_info)
  )
  new_eqn = pe.new_jaxpr_eqn(
      eqn.invars, outvars, eqn.primitive, new_params,
      core.eqn_effects(dce_call_jaxpr, eqn.invars),
      eqn.source_info, eqn.ctx)
  return used_ins, new_eqn

