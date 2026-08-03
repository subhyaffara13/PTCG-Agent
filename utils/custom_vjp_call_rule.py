import functools

def custom_vjp_call_rule(in_err, enabled_errors, *in_vals,
                         call_jaxpr: core.ClosedJaxpr,
                         fwd_jaxpr_thunk, num_consts,
                         bwd: lu.WrappedFun, out_trees,
                         symbolic_zeros: bool):
  err_vals, err_tree = jtu.tree_flatten(in_err)
  num_errs = err_tree.num_leaves
  checkified_fun = lu.wrap_init(
      functools.partial(checkify_jaxpr_flat, call_jaxpr.jaxpr,
                        call_jaxpr.consts, enabled_errors, err_tree),
      debug_info=call_jaxpr.jaxpr.debug_info)
  checkified_fun, fun_metadata = _flatten_and_get_error_metadata_thunk(
      checkified_fun)

  def checkified_fwd(*args):
    # TODO(lenamartens, sharadmv): why not checkify here?
    xs, zeros = args[::2], args[1::2]
    xs, zeros = xs[num_errs:], zeros[num_errs:]
    fwd_jaxpr, fwd_consts = fwd_jaxpr_thunk.call_wrapped(*zeros)
    xs_without_consts = xs[num_consts:]
    return core.eval_jaxpr(fwd_jaxpr, fwd_consts, *xs_without_consts)

  # TODO(necula): the fwd result_paths are not quite the same as fun_jaxpr
  checkified_fwd_wrapped = lu.wrap_init(checkified_fwd,
                                        debug_info=fwd_jaxpr_thunk.debug_info)
  bwd_ = lu.wrap_init(lambda *args: (*(None,)*num_errs, *bwd.call_wrapped(*args)),
                      debug_info=bwd.debug_info)
  checkified_fwd_wrapped, fwd_out_tree = flatten_fun_output(checkified_fwd_wrapped)
  all_outs = custom_derivatives.custom_vjp_call_p.bind(
      *err_vals, *in_vals, out_trees=out_trees, symbolic_zeros=symbolic_zeros,
      subfuns=(checkified_fun, checkified_fwd_wrapped, bwd_))
  fst, out_metadata = lu.merge_linear_aux(fun_metadata, fwd_out_tree)
  if fst:
    err_and_out_tree, _ = out_metadata
    out_err, out_vals = tree_unflatten(err_and_out_tree, all_outs)
  else:
    out_err, out_vals = in_err, all_outs
  return out_err, out_vals

