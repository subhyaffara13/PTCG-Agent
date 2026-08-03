from typing import Callable

def trace_to_subjaxpr_nounits_fwd(
    f: Callable,
    tag: TraceTag,
    debug_info: core.DebugInfo,
    instantiate: bool | Sequence[bool],
    in_pvals: Sequence[PartialVal]):
  assert all(isinstance(pv, PartialVal) for pv in in_pvals), in_pvals
  current_name_stack = source_info_util.current_name_stack()
  with core.take_current_trace() as parent_trace:
    trace = JaxprTrace(parent_trace, current_name_stack, tag)
    with core.set_current_trace(trace):
      out_tracers, jaxpr, out_consts, env = _trace_to_subjaxpr_nounits(
          f, trace, instantiate, in_pvals, debug_info)
    out_pvals = [t.pval for t in out_tracers]

    # Which out_consts (aka residuals) are just forwarded inputs? Check obj id.
    in_consts  = [pval.get_known()    for pval in in_pvals if     pval.is_known()]
    id_map = {id(c): i for i, c in enumerate(in_consts)}
    fwds: list[int | None] = [id_map.get(id(c)) for c in out_consts]
    pruned_consts = [c for c, fwd in zip(out_consts, fwds) if fwd is None]

    del out_tracers
  return jaxpr, (fwds, out_pvals, pruned_consts, env)

