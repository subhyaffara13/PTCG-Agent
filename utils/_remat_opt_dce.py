
def _remat_opt_dce(used_outs: list[bool], eqn: core.JaxprEqn):
  if not any(used_outs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None
  used_res, used_prims = split_list(used_outs, [eqn.params["num_res"]])
  outvars = [v for used, v in zip(used_outs, eqn.outvars) if used]
  if any(used_res):
    # If any of the residuals are used, we still need to run fwd at this point,
    # but we may end up DCEing again in the future, so we must instantiate all
    # the input primals.
    instantiate = [False] * eqn.params["num_consts"]
    instantiate += [True] * (len(eqn.invars) - eqn.params["num_consts"])
    new_jaxpr, used_ins = pe.dce_jaxpr(eqn.params["fwd_jaxpr"].jaxpr, used_outs,
                                       instantiate=instantiate)
    assert not new_jaxpr.constvars
    closed_jaxpr = pe.close_jaxpr(new_jaxpr)
    invars = [v for used, v in zip(used_ins, eqn.invars) if used]
    new_params = dict(eqn.params)
    new_num_consts = sum(split_list(used_ins, [eqn.params["num_consts"]])[0])
    new_params["num_consts"] = new_num_consts
    new_params["fwd_jaxpr"] = closed_jaxpr
    new_params["num_res"] = sum(used_res)
    new_eqn = pe.new_jaxpr_eqn(
        invars, outvars, remat_opt_p, new_params,
        core.eqn_effects(closed_jaxpr, invars),
        eqn.source_info, eqn.ctx)
    return used_ins, new_eqn
  else:
    # If none of the residuals are used, we run the primal computation instead.
    # At this point we drop this custom DCE behavior, but since the primal might
    # have different consts than fwd, we build a new JaxprEqn with a closed_call
    # primitive.
    fun_jaxpr, consts = eqn.params["fun_jaxpr_thunk"]()
    new_jaxpr, used_consts, used_ins = pe.dce_jaxpr_consts(fun_jaxpr, used_prims)
    consts = [c for used, c in zip(used_consts, consts) if used]
    closed_jaxpr = core.ClosedJaxpr(new_jaxpr, consts)
    _, invars = split_list(eqn.invars, [eqn.params["num_consts"]])
    invars = [v for used, v in zip(used_ins, invars) if used]
    new_eqn = pe.new_jaxpr_eqn(
        invars, outvars, core.closed_call_p, dict(call_jaxpr=closed_jaxpr),
        core.eqn_effects(closed_jaxpr, invars), eqn.source_info, eqn.ctx)
    used_ins = [False] * eqn.params["num_consts"] + used_ins
    return used_ins, new_eqn

