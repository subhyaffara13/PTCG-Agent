
def remat_error_check(error, enabled_errors, *vals_in, jaxpr, **params):
  err_vals, err_tree = jtu.tree_flatten(error)
  new_vals_in = [*err_vals, *vals_in]
  in_avals = tuple(map(core.typeof, new_vals_in))
  checked_jaxpr_, out_tree, _ = jaxpr_to_checkify_jaxpr(
      pe.close_jaxpr(jaxpr), enabled_errors, err_tree, *in_avals)
  checked_jaxpr, () = checked_jaxpr_.jaxpr, checked_jaxpr_.consts
  err_and_out = ad_checkpoint.remat_p.bind(*new_vals_in, jaxpr=checked_jaxpr,
                                           **params)
  return tree_unflatten(out_tree, err_and_out)

