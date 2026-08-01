
def checkify_jaxpr(jaxpr: core.ClosedJaxpr, enabled_errors,
                   error: Error, *args) -> tuple[Error, list[core.Value]]:
  err_vals, err_tree = jtu.tree_flatten(error)
  return checkify_jaxpr_flat(jaxpr.jaxpr, jaxpr.consts,
                             enabled_errors, err_tree, *err_vals, *args)

