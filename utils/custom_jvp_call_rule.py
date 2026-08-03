import functools

def custom_jvp_call_rule(in_err: Error,
                         enabled_errors: set, *in_vals, num_consts,
                         jvp_jaxpr_fun: lu.WrappedFun,
                         call_jaxpr: core.ClosedJaxpr, **params):
  # The types to have in mind are:
  #   jvp : (a -> b) -> (a, T a) -> (b, T b)
  #   checkify : (a -> b) -> a -> Err b
  #   jvp-of-checkify : (a -> b) -> (a, T a) -> (Err b, T (Err b))
  # where because Err is a pytree, we necessarily have T (Err b) = Err' (T b)
  # where the other Err' components are trivial (of float0 dtype).
  # Semantically, we don't add checks to the JVP rule. To check the result of a
  # JVP rule, one must instead use checkify-of-jvp. Thus this implementation
  # just forwards the input error and code (and trivial tangents) to the output.
  err_vals, err_tree = jtu.tree_flatten(in_err)
  partial_checkify = lu.wrap_init(
      functools.partial(checkify_jaxpr_flat, call_jaxpr.jaxpr,
                        call_jaxpr.consts, enabled_errors, err_tree),
      debug_info=call_jaxpr.jaxpr.debug_info)
  partial_checkify, f_metadata = _flatten_and_get_error_metadata_thunk(
      partial_checkify)
  jvp = lift_jvp(err_tree.num_leaves, num_consts, jvp_jaxpr_fun)
  jvp, jvp_out_tree = flatten_fun_output(jvp)
  all_outs = custom_derivatives.custom_jvp_call_p.bind(
      *err_vals, *in_vals, subfuns=(partial_checkify, jvp), **params)
  fst, out_metadata = lu.merge_linear_aux(f_metadata, jvp_out_tree)
  if fst:
    err_and_out_tree, _ = out_metadata
    out_err, out_vals = tree_unflatten(err_and_out_tree, all_outs)
  else:
    err_vals, out_vals = split_list(all_outs, [len(err_vals)])
    # forward input error to output
    out_err = jtu.tree_unflatten(err_tree, err_vals)
  return out_err, out_vals

