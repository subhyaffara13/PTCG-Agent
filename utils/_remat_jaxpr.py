
def _remat_jaxpr(jaxpr, policy):
  dbg = jaxpr.jaxpr.debug_info
  fwd_trace = pe.DynamicJaxprTrace(dbg)
  rem_trace = pe.DynamicJaxprTrace(dbg, auto_dce=True)
  tag = core.TraceTag()
  trace = RematTrace(fwd_trace, rem_trace, tag, policy)
  rem_trace.tag = tag
  src = source_info_util.current()

  def new_arg(a):
    return RematTracer(trace, fwd_trace.new_arg(a, src), rem_trace.new_arg(a, src))  # noqa: F821

  tracers = map(new_arg, jaxpr.in_aval_qdds)
  with core.set_current_trace(trace, check_leaks=True):
    ans = core.eval_jaxpr(jaxpr.jaxpr, jaxpr.consts, *tracers)
    out_primals, out_rem = unzip2(map(trace.to_val_tracer_pair, ans))
    del trace, ans, new_arg, tracers

  out_rem = [rem_trace.to_jaxpr_tracer(x, source_info=src) for x in out_rem]
  rem_jaxpr_, rem_consts = rem_trace.to_jaxpr(out_rem, dbg.with_unknown_names(), src)
  rem_jaxpr = pe.close_jaxpr(pe.convert_constvars_jaxpr(rem_jaxpr_))
  rem_trace.invalidate()

  rem_consts = map(partial(fwd_trace.to_jaxpr_tracer, source_info=src), rem_consts)
  out_primals = [fwd_trace.to_jaxpr_tracer(x, source_info=src) for x in out_primals]
  fwd_jaxpr_, fwd_consts = fwd_trace.to_jaxpr(
      [*out_primals, *rem_consts], dbg.with_unknown_names(), src)
  fwd_trace.invalidate()

  fwd_jaxpr = core.ClosedJaxpr(fwd_jaxpr_, fwd_consts)
  return fwd_jaxpr, rem_jaxpr, len(rem_consts)

