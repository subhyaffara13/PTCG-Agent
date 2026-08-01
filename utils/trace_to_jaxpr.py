
def trace_to_jaxpr(
    fun: Callable,
    in_avals: FlatTree,  # (args, kwargs) pair
    debug_info: core.DebugInfo,
    *context_for_cache_key,
    # TODO: let's just make a `trace_to_jaxpr_ft` function for this
    fun_takes_flat_tree_arg=False,
    fun_returns_flat_tree=False,
    requires_low=False,
) -> tuple[ClosedJaxpr, FlatTree]:
  if config.no_tracing.value:
    raise RuntimeError(f"re-tracing function {fun} for "
                       "`jit`, but 'no_tracing' is set")
  del context_for_cache_key  # read implicitly, e.g. qdd state
  test_event("trace_to_jaxpr")
  config.enable_checks.value and debug_info.assert_arg_names(len(in_avals))
  parent_trace = core.trace_ctx.trace
  trace = DynamicJaxprTrace(debug_info, parent_trace=parent_trace,
                            lower=requires_low)
  # Name stack and the traceback scope are reset because the metadata on jaxpr
  # equations should be rooted at the enclosing jaxpr and not contain any
  # context from the callsite. Otherwise metadata from one caller would bleed
  # into metadata from a different caller if we, e.g., inline.
  with (core.ensure_no_leaks(trace), source_info_util.reset_name_stack(),
        TracebackScope()):
    source_info = source_info_util.current()
    if requires_low:
      def new_arg(aval):
        lo_tracers = [trace.new_arg(lo_aval, source_info=source_info) for lo_aval in aval.lo_ty()]  # noqa: F821
        return aval.raise_val(*lo_tracers)
      in_tracers = in_avals.map(new_arg)
    else:
      in_tracers = in_avals.map(partial(trace.new_arg, source_info=source_info))

    with core.set_current_trace(trace):
      if fun_takes_flat_tree_arg:
        args_ft, kwargs_ft = in_tracers.unpack()
        assert kwargs_ft.unflatten() == {}  # TODO: handle kwargs
        kwargs = {}
        args = args_ft.unpack()
        del args_ft
      else:
        args, kwargs = in_tracers.unflatten()
      ans_pytree = fun(*args, **kwargs)
      if fun_returns_flat_tree:
        # TODO(dougalm): make result paths optional
        ans = ans_pytree
        debug_info = debug_info.set_result_paths([''] * len(ans))
      else:
        debug_info = debug_info.set_result_paths(ans_pytree)
        ans = FlatTree.flatten(ans_pytree)
      del ans_pytree, args, kwargs

    _check_returned_jaxtypes(debug_info, list(ans))
    ans = ans.map(dtypes.canonicalize_value)
    out_avals = ans.map(typeof)
    if requires_low:
      flat_out_tracers = [trace.to_jaxpr_tracer(x, source_info=source_info)
                          for aval, hi_val in zip(out_avals, ans)
                          for x in aval.lower_val(hi_val)]
    else:
      flat_out_tracers = [trace.to_jaxpr_tracer(x, source_info=source_info)
                          for x in ans]

    _check_no_returned_refs(debug_info, list(flat_out_tracers))
    jaxpr, consts = trace.frame.to_jaxpr(trace, list(flat_out_tracers), debug_info,
                                         source_info)
    del trace, fun, in_tracers, flat_out_tracers, ans
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  return ClosedJaxpr(jaxpr, consts), out_avals

