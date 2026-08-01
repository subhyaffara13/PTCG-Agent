
def _linearize_jaxpr(
    jaxpr: core.ClosedJaxpr,
    nonzeros: tuple[bool, ...],
    instantiate: tuple[bool, ...],
    allow_fwds: tuple[bool, ...],
    is_vjp: bool,
) -> tuple[core.ClosedJaxpr, int, Sequence[bool], Sequence[int | None], core.ClosedJaxpr]:
  dbg = jaxpr.jaxpr.debug_info
  config.enable_checks.value and dbg.assert_arg_names(len(nonzeros))
  primal_trace = pe.DynamicJaxprTrace(dbg)
  tangent_trace = pe.DynamicJaxprTrace(dbg, auto_dce=True)
  tag = core.TraceTag()
  tangent_trace.tag = tag
  lin_trace = LinearizeTrace(primal_trace, tangent_trace, is_vjp=is_vjp)

  def new_arg(trace, primal_aval, nz, source_info):
    primal = primal_trace.new_arg(primal_aval, source_info)
    tangent_aval = primal_aval.to_tangent_aval()
    tangent = tangent_trace.new_arg(tangent_aval, source_info) if nz else Zero(tangent_aval)
    return LinearizeTracer(trace, primal, tangent)

  source_info = source_info_util.current()
  tracers = [new_arg(lin_trace, a, nz, source_info)
             for (a, nz) in zip(jaxpr.in_aval_qdds, nonzeros)]
  in_primals = [t.primal for t in tracers]

  with core.set_current_trace(lin_trace, check_leaks=True):
    ans = core.eval_jaxpr(jaxpr.jaxpr, jaxpr.consts, *tracers)
    out_primals, out_tangents = unzip2(map(lin_trace.to_primal_tangent_pair, ans))
    out_tangents = [instantiate_zeros(t) if inst else t
                    for t, inst in zip(out_tangents, instantiate)]
    del lin_trace, ans, new_arg, tracers

  # pe._check_no_returned_refs(debug_info, out_tangents)
  nzs_out = [type(t) is not Zero for t in out_tangents]
  out_tangents = [tangent_trace.to_jaxpr_tracer(t, source_info)
                  for (nz, t) in zip(nzs_out, out_tangents) if nz]
  tangent_jaxpr, tangent_consts = tangent_trace.to_jaxpr(
      out_tangents, dbg.with_unknown_names(), source_info)
  tangent_trace.invalidate()
  tangent_jaxpr, tangent_consts = _dce_consts(tangent_jaxpr, tangent_consts)
  tangent_jaxpr = pe.close_jaxpr(pe.convert_constvars_jaxpr(tangent_jaxpr))

  fwd_inputs = (*jaxpr.consts, *in_primals)
  id_map = {id(x):i for i, (x,a) in enumerate(zip(fwd_inputs, allow_fwds)) if a}
  fwds = [id_map.get(id(c)) for c in tangent_consts]
  tangent_consts = [c for c, f in zip(tangent_consts, fwds) if f is None]
  del in_primals

  # pe._check_no_returned_refs(debug_info, out_primals)
  primals_and_residuals = *out_primals, *tangent_consts
  primals_and_residuals = map(partial(primal_trace.to_jaxpr_tracer, source_info=source_info),
                              primals_and_residuals)
  primal_jaxpr, primal_consts = primal_trace.to_jaxpr(
      primals_and_residuals, dbg.with_unknown_names(),
      source_info)
  primal_trace.invalidate()
  primal_jaxpr, primal_consts = _dce_consts(primal_jaxpr, primal_consts)
  primal_jaxpr = core.ClosedJaxpr(primal_jaxpr, primal_consts)

  num_residuals_out = len(tangent_consts)
  return primal_jaxpr, num_residuals_out, nzs_out, fwds, tangent_jaxpr

