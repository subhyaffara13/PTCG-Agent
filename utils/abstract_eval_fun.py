from typing import Callable

def abstract_eval_fun(fun: Callable, *avals,
                      debug_info: core.DebugInfo, **params):
  _, avals_out, _ = trace_to_jaxpr_dynamic(
      lu.wrap_init(fun, params, debug_info=debug_info), avals)
  assert all(isinstance(aval, AbstractValue) for aval in avals_out)
  return avals_out

