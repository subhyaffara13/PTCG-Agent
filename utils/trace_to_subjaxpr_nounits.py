from typing import Callable

def trace_to_subjaxpr_nounits(
    f: Callable,
    trace: JaxprTrace,
    instantiate: Sequence[bool] | bool,
    debug_info: core.DebugInfo,
    in_pvals: Sequence[PartialVal]):
  assert all(isinstance(pv, PartialVal) for pv in in_pvals), in_pvals
  out_tracers, jaxpr, out_consts, env = _trace_to_subjaxpr_nounits(
      f, trace, instantiate, in_pvals, debug_info)
  out_pvals = [t.pval for t in out_tracers]
  del out_tracers
  return jaxpr, (out_pvals, out_consts, env)

