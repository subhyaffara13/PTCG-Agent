from typing import Callable

def trace_to_subjaxpr_nounits2(
    f: Callable,
    tag: TraceTag,
    debug_info: core.DebugInfo,
    instantiate: bool | Sequence[bool],
    in_pvals: Sequence[PartialVal]):
  assert isinstance(tag, TraceTag)
  assert all(isinstance(pv, PartialVal) for pv in in_pvals), in_pvals
  current_name_stack = source_info_util.current_name_stack()
  with core.take_current_trace() as parent_trace:
    trace = JaxprTrace(parent_trace, current_name_stack, tag)
    out_tracers, jaxpr, out_consts, env = _trace_to_subjaxpr_nounits(
        f, trace, instantiate, in_pvals, debug_info)
    out_pvals = [t.pval for t in out_tracers]
    del out_tracers
  return jaxpr, (out_pvals, out_consts, env)

