from typing import Any, Callable

def _trace_to_jaxpr(fun, in_tree, in_avals, dbg):
  f = lu.wrap_init(fun, debug_info=dbg)
  f, out_tree = flatten_fun_nokwargs(f, in_tree)
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(f, in_avals)
  return core.ClosedJaxpr(jaxpr, consts), out_tree()


def _trace_to_jaxpr(fun: Callable,
                    in_tree: PyTreeDef,
                    in_avals: Sequence[core.AbstractValue],
                    debug: core.DebugInfo
                    ) -> tuple[core.Jaxpr, Sequence[Any], PyTreeDef]:
  in_avals_flat_tree = FlatTree(in_avals, in_tree, False)
  try:
    closed_jaxpr, out_avals = pe.trace_to_jaxpr(fun, in_avals_flat_tree, debug)
  except core.ConcretizationTypeError as e:
    msg, = e.args
    if 'for checkpoint' in msg:
      msg += "\n\n" + (
          "Consider using the `static_argnums` parameter for `jax.remat` or "
          "`jax.checkpoint`. See the `jax.checkpoint` docstring and its example "
          "involving `static_argnums`:\n"
          "https://docs.jax.dev/en/latest/_autosummary/jax.checkpoint.html"
          "\n")
      e.args = msg,
    raise
  return pe.convert_constvars_jaxpr(closed_jaxpr.jaxpr), closed_jaxpr.consts, out_avals.tree


def _trace_to_jaxpr(fun, in_avals, in_tree, dbg):
  f = lu.wrap_init(fun, debug_info=dbg)
  f, out_tree = flatten_fun_nokwargs(f, in_tree)
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(f, in_avals)
  return core.ClosedJaxpr(jaxpr, consts), out_tree()

