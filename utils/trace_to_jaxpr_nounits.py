
def trace_to_jaxpr_nounits(
    fun: lu.WrappedFun, pvals: Sequence[PartialVal],
    instantiate: bool | Sequence[bool] = False,
  ) -> tuple[Jaxpr, list[PartialVal], list[core.Value]]:
  current_name_stack = source_info_util.current_name_stack()
  with core.take_current_trace() as parent_trace:
    trace = JaxprTrace(parent_trace, current_name_stack, TraceTag())
    with core.ensure_no_leaks(trace):
      fun = trace_to_subjaxpr_nounits(fun, trace, instantiate, fun.debug_info)
      with core.set_current_trace(trace):
        jaxpr, (out_pvals, consts, env) = fun.call_wrapped(pvals)
        assert not env
      del trace, fun
      return jaxpr, out_pvals, consts

