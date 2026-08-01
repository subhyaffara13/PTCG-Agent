
def call_hi_primitive_error_check(error, enabled_errors, *vals_in, _prim):
  if not isinstance(_prim, ad_checkpoint.RematTraced):
    return default_checkify_rule(call_hi_primitive_p, error, enabled_errors,
                                 *vals_in, _prim=_prim)
  err_vals, err_tree = jtu.tree_flatten(error)
  new_vals_in = [*err_vals, *vals_in]
  in_avals = tuple(map(core.typeof, new_vals_in))
  checked_jaxpr_, out_tree, _ = jaxpr_to_checkify_jaxpr(
      _prim.jaxpr, enabled_errors, err_tree, *in_avals)
  checked_jaxpr, consts = pe.separate_consts(checked_jaxpr_)
  new_prim = ad_checkpoint.RematTraced(checked_jaxpr, _prim.policy)
  err_and_out = new_prim(*consts, *new_vals_in)
  return tree_unflatten(out_tree, err_and_out)

