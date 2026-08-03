from typing import Any

def trace_to_jaxpr_dynamic(
    fun: lu.WrappedFun, in_avals: Sequence[AbstractValue | core.AvalQDD],
    *, keep_inputs: list[bool] | None = None, lower: bool = False,
    auto_dce: bool = False) -> tuple[Jaxpr, list[AbstractValue], list[Any]]:
  config.enable_checks.value and fun.debug_info.assert_arg_names(len(in_avals))
  keep_inputs = [True] * len(in_avals) if keep_inputs is None else keep_inputs
  parent_trace = core.trace_ctx.trace
  trace = DynamicJaxprTrace(fun.debug_info, parent_trace=parent_trace,
                            lower=lower, auto_dce=auto_dce)
  # Name stack and the traceback scope are reset because the metadata on jaxpr
  # equations should be rooted at the enclosing jaxpr and not contain any
  # context from the callsite. Otherwise metadata from one caller would bleed
  # into metadata from a different caller if we, e.g., inline.
  with (core.ensure_no_leaks(trace), source_info_util.reset_name_stack(),
        TracebackScope()):
    source_info = source_info_util.current()
    in_tracers = map(partial(trace.new_arg, source_info=source_info), in_avals)
    in_tracers = [t for t, keep in zip(in_tracers, keep_inputs) if keep]
    with core.set_current_trace(trace):
      ans = fun.call_wrapped(*in_tracers)
    _check_returned_jaxtypes(fun.debug_info, ans)
    ans = map(dtypes.canonicalize_value, ans)
    out_tracers = map(partial(trace.to_jaxpr_tracer, source_info=source_info), ans)
    _check_no_returned_refs(fun.debug_info, out_tracers)
    jaxpr, consts = trace.frame.to_jaxpr(trace, out_tracers, fun.debug_info,
                                         source_info)
    del trace, fun, in_tracers, out_tracers, ans
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  return jaxpr, [v.aval for v in jaxpr.outvars], consts

