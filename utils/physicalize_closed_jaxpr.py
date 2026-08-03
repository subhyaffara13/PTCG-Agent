import functools

def physicalize_closed_jaxpr(jaxpr: core.ClosedJaxpr) -> core.ClosedJaxpr:
  """Replaces all extended dtypes with physical types in a jaxpr."""
  fun = functools.partial(physicalize_interp, jaxpr.jaxpr, jaxpr.consts)
  in_avals = [_physical_aval(aval) for aval in jaxpr.in_avals]
  flat_avals, treedef = tree_util.tree_flatten(in_avals)
  debug_info = api_util.debug_info("physicalize_closed_jaxpr", fun, (), {})
  wrapped_fun, _ = api_util.flatten_fun_nokwargs(
      lu.wrap_init(fun, debug_info=debug_info.with_unknown_names()), treedef
  )
  new_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, flat_avals)
  assert len(new_jaxpr.constvars) == len(consts), "Mismatched consts"
  return core.ClosedJaxpr(new_jaxpr, consts)

