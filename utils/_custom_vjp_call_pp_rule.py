
def _custom_vjp_call_pp_rule(eqn: core.JaxprEqn,
                             context: core.JaxprPpContext,
                             settings: core.JaxprPpSettings) -> core.pp.Doc:
  params = dict(eqn.params)
  if not params["num_consts"]:
    params.pop("num_consts")
  params.pop("out_trees")
  params["fwd"] = params.pop("fwd_jaxpr_thunk").debug_info.func_name
  params["bwd"] = params.pop("bwd").debug_info.func_name
  names = sorted(params)
  params["name"] = params["call_jaxpr"].jaxpr.debug_info.func_name
  return core._pp_eqn(eqn.replace(params=params), context, settings,
                      params=["name"] + names)

