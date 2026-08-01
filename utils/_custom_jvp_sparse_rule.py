
def _custom_jvp_sparse_rule(spenv, *spvalues, **params):
  call_jaxpr: core.ClosedJaxpr = params.pop('call_jaxpr')
  jvp_jaxpr_fun: lu.WrappedFun = params.pop('jvp_jaxpr_fun')
  num_consts: int = params.pop('num_consts')
  sp_call_jaxpr, out_tree = _sparsify_jaxpr(spenv, call_jaxpr, *spvalues)
  def fun(*flat_arrs):
    arrs = tree_util.tree_unflatten(out_tree, flat_arrs)
    sparrs = arrays_to_spvalues(spenv, arrs)
    out = eval_sparse(call_jaxpr.jaxpr, call_jaxpr.consts, sparrs, spenv)
    return tree_util.tree_flatten(spvalues_to_arrays(spenv, out))[0]
  jvp = lift_jvp(num_consts, jvp_jaxpr_fun)
  invals = spvalues_to_arrays(spenv, spvalues)
  flat_invals, _ = tree_util.tree_flatten(invals)

  flat_outvals = jax.custom_derivatives.custom_jvp_call_p.bind(
      *flat_invals,
      subfuns=(lu.wrap_init(fun, debug_info=call_jaxpr.jaxpr.debug_info), jvp),
      **params)
  outvals = tree_util.tree_unflatten(out_tree, flat_outvals)
  return arrays_to_spvalues(spenv, outvals)

