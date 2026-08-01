
def checkify_while_body_jaxpr(
    cond_jaxpr: core.ClosedJaxpr, body_jaxpr: core.ClosedJaxpr,
    enabled_errors, error: Error,
    c_consts_num: int) -> tuple[core.ClosedJaxpr, PyTreeDef, set[ErrorEffect]]:
  cond_f = core.jaxpr_as_fun(cond_jaxpr)
  body_f = core.jaxpr_as_fun(body_jaxpr)
  def new_body_f(*c_consts_and_vals):
    c_consts, vals = split_list(c_consts_and_vals, [c_consts_num])
    out = body_f(*vals)
    # This checks if the next cond application will error
    lax.dce_sink(cond_f(*c_consts, *out))
    return out
  c_consts_avals = cond_jaxpr.in_avals[:c_consts_num]

  jaxpr, _ = pe.trace_to_jaxpr(
      new_body_f,
      FlatTree.flatten(((*c_consts_avals, *body_jaxpr.in_avals), {})),
      debug_info=body_jaxpr.jaxpr.debug_info.with_unknown_names())
  err_vals, err_tree = jtu.tree_flatten(error)
  err_vals = map(core.typeof, err_vals)
  flat_err_and_in_vals = [*err_vals, *c_consts_avals, *body_jaxpr.in_avals]
  jaxpr, out_tree, error_effects = jaxpr_to_checkify_jaxpr(
      jaxpr, enabled_errors, err_tree, *flat_err_and_in_vals)
  return jaxpr, out_tree, error_effects

