
def _custom_lin_pp_rule(eqn: core.JaxprEqn, context: core.JaxprPpContext,
                        settings: core.JaxprPpSettings) -> core.pp.Doc:
  params = dict(eqn.params)
  params.pop("out_avals")
  params["bwd"] = params.pop("bwd").debug_info.func_name
  return core._pp_eqn(eqn.replace(params=params), context, settings)

