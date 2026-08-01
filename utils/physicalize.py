
def physicalize(f):
  """Runs a function that contains fusible extended dtypes."""

  def wrapper(*args, **kwargs):
    if kwargs:
      raise NotImplementedError()
    flattened_args, treedef = jax.tree.flatten(args)
    debug_info = api_util.debug_info("physicalize", f, args, kwargs)
    wrapped_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
        lu.wrap_init(f, debug_info=debug_info), treedef
    )
    avals = [core.typeof(a) for a in flattened_args]
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, avals)
    new_jaxpr = physicalize_closed_jaxpr(core.ClosedJaxpr(jaxpr, consts))
    out_flat = core.eval_jaxpr(
        new_jaxpr.jaxpr, new_jaxpr.consts, *flattened_args
    )
    return tree_util.tree_unflatten(out_tree_thunk(), out_flat)

  return wrapper

