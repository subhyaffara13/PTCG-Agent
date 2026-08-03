from typing import Callable

def trace_to_subjaxpr_nounits_fwd2(
    f: Callable,
    tag: TraceTag,
    debug_info: core.DebugInfo,
    instantiate: bool | Sequence[bool],
    in_pvals: Sequence[PartialVal]):
  assert all(isinstance(pv, PartialVal) for pv in in_pvals), in_pvals
  current_name_stack = source_info_util.current_name_stack()
  with core.take_current_trace() as parent_trace:
    trace = JaxprTrace(parent_trace, current_name_stack, tag)
    out_tracers, jaxpr, consts, env = _trace_to_subjaxpr_nounits_no_lu_2(
        f, trace, instantiate, in_pvals, debug_info)
    out_pvals = out_tracers.map(lambda t: t.pval)

  # Which consts (aka residuals) are just forwarded inputs? Check obj id.
  in_consts  = [pval.get_known()    for pval in  in_pvals if    pval.is_known()]
  id_map = {id(c): i for i, c in enumerate(in_consts)}
  input_fwds: list[int | None] = [id_map.get(id(c)) for c in consts]

  # Which consts (aka residuals) are already primal outputs? Check obj id.
  out_consts = [pval.get_known()    for pval in out_pvals if    pval.is_known()]
  id_map = {id(c): i for i, c in enumerate(out_consts)}
  output_fwds: list[int | None] = [id_map.get(id(c)) for c in consts]

  pruned_consts = [c for c, f1, f2 in zip(consts, input_fwds, output_fwds)
                   if f1 is None and f2 is None]

  del out_tracers
  return jaxpr, (input_fwds, output_fwds, out_pvals, pruned_consts, env)

