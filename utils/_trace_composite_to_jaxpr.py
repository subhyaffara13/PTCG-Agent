
def _trace_composite_to_jaxpr(fun: Callable,
                              in_tree: tree_util.PyTreeDef,
                              in_avals: Sequence[core.AbstractValue],
                              name: str,
                              debug_info: core.DebugInfo):

  def flat_fun(*flat_args):
    args = tree_util.tree_unflatten(in_tree, flat_args)
    return fun(*args)

  in_avals_flat_tree = tree_util.FlatTree.flatten_args(*in_avals)
  closed_jaxpr, out_avals = pe.trace_to_jaxpr(
      flat_fun, in_avals_flat_tree, debug_info
  )
  consts = closed_jaxpr.consts
  if any(isinstance(c, core.Tracer) for c in consts):
    raise UnexpectedTracerError(
        "Found a JAX Tracer as a constant in the decomposition for the "
        f"composite op '{name}'. This means that the decomposition function "
        "closes over a value that is involved in a JAX transformation. "
        "Any values that aren't explicitly known at compile time must be "
        "explicitly passed as arguments to the composite.")
  # Absorb consts into jaxpr invars (matching behavior of old convert_constvars_jaxpr)
  closed_jaxpr = pe.close_jaxpr(pe.convert_constvars_jaxpr(closed_jaxpr.jaxpr))
  return closed_jaxpr, consts, out_avals.tree

