
def jaxpr_to_checkify_jaxpr(
    jaxpr: core.ClosedJaxpr, enabled_errors, err_tree: PyTreeDef,
    *flat_err_and_in_vals) -> tuple[core.ClosedJaxpr, PyTreeDef, set[ErrorEffect]]:

  def fun_wrapped(*invals):
    error, out = checkify_jaxpr_flat(
        jaxpr.jaxpr, jaxpr.consts, enabled_errors, err_tree, *invals)
    error_effects = ErrorEffects(set(error._pred.keys()))
    return (error, out), error_effects

  debug_info = jaxpr.jaxpr.debug_info.with_unknown_names()
  args_avals = FlatTree.flatten((flat_err_and_in_vals, {}))
  checked_jaxpr, full_out_avals = pe.trace_to_jaxpr(fun_wrapped, args_avals, debug_info)
  out_avals, error_effects = full_out_avals.unpack()
  error_effects = error_effects.unflatten().val
  return checked_jaxpr, out_avals.tree, error_effects

