from typing import Any, Callable

def _initial_style_jaxpr(fun: lu.WrappedFun,
                         in_avals: Sequence[core.AbstractValue]
                         ) -> tuple[core.Jaxpr, Sequence[Any]]:
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun, in_avals)
  return jaxpr, consts


def _initial_style_jaxpr(fun: Callable,
                         in_tree: api_util.PyTreeDef,
                         in_avals: Sequence[core.AbstractValue],
                         debug: core.DebugInfo):
  fun_, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(fun, debug_info=debug),
      tree_util.treedef_tuple((in_tree,)))
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun_, in_avals)
  return jaxpr, consts, out_tree_thunk()

