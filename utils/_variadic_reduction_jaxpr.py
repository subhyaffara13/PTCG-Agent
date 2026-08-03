from typing import Any, Callable

def _variadic_reduction_jaxpr(computation: Callable[[Any, Any], Any],
                              debug_info: core.DebugInfo,
                              flat_avals,
                              aval_tree: tree_util.PyTreeDef):
  avals = tree_util.tree_unflatten(aval_tree, flat_avals)
  flat_in_avals, in_tree = tree_util.tree_flatten((avals, avals))
  def flat_computation(*flat_args):
    xs, ys = tree_util.tree_unflatten(in_tree, flat_args)
    return computation(xs, ys)

  in_avals_flat_tree = tree_util.FlatTree.flatten_args(*flat_in_avals)
  closed_jaxpr, out_avals = pe.trace_to_jaxpr(
      flat_computation, in_avals_flat_tree, debug_info
  )
  if any(isinstance(c, core.Tracer) for c in closed_jaxpr.consts):
    raise NotImplementedError(
        "Reduction computations can't close over Tracers. Please open an issue "
        "at https://github.com/jax-ml/jax.")
  return closed_jaxpr, out_avals.tree

