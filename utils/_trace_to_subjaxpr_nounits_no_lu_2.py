
def _trace_to_subjaxpr_nounits_no_lu_2(f: Callable, trace: JaxprTrace,
                               instantiate: Sequence[bool] | bool,
                               in_pvals: Sequence[PartialVal],
                               debug_info: core.DebugInfo):
  in_knowns  = [pval.is_known()     for pval in in_pvals]
  in_consts  = [pval.get_known()    for pval in in_pvals if     pval.is_known()]
  in_tracers = [trace.new_arg(pval) for pval in in_pvals if not pval.is_known()]
  in_args = merge_lists(in_knowns, in_tracers, in_consts)
  with core.set_current_trace(trace):
    ans = f(*in_args)
  assert isinstance(ans, FlatTree), (
      f"Got unexpected return type when tracing function to jaxpr: {ans}")
  assert all(isinstance(x, Tracer) or core.valid_jaxtype(x) for x in ans), (
      f"Got unexpected return type when tracing function to jaxpr: {ans}")
  if isinstance(instantiate, bool):
    instantiate = [instantiate] * len(ans)
  out_tracers = ans.map(trace.to_jaxpr_tracer)
  out_tracers = out_tracers.map2(
      lambda t, inst: trace.instantiate_const(t) if inst else t, instantiate)
  out_tracers_ = [t for t in out_tracers if not t.is_known()]
  jaxpr, out_consts, env = tracers_to_jaxpr(
      in_tracers, out_tracers_, trace.effect_handles,
      debug_info.with_unknown_names())
  return out_tracers, jaxpr, out_consts, env

