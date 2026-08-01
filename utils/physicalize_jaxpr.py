
def physicalize_jaxpr(jaxpr: core.Jaxpr) -> core.Jaxpr:
  """Replaces all extended dtypes with physical types in a jaxpr."""

  def _flat_jaxpr_eval(consts, args):
    return physicalize_interp(jaxpr, consts, *args)

  in_avals = [_physical_aval(v.aval) for v in jaxpr.invars]
  const_avals = [_physical_aval(v.aval) for v in jaxpr.constvars]
  flat_avals, treedef = jax.tree.flatten((const_avals, in_avals))
  debug_info = api_util.debug_info(
      "physicalize_jaxpr", _flat_jaxpr_eval, (const_avals, in_avals), {})
  wrapped_fun, _ = api_util.flatten_fun_nokwargs(
      lu.wrap_init(_flat_jaxpr_eval, debug_info=debug_info), treedef
  )
  new_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, flat_avals)
  assert not consts
  new_jaxpr = pe.convert_invars_to_constvars(
      new_jaxpr, len(tree_util.tree_leaves(const_avals))
  )
  return new_jaxpr

