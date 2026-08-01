
def linearize_subtrace(_f: Callable, _store: lu.Store, _is_vjp: bool,
                       _tag: core.TraceTag, nzs_in: Sequence[bool],
                       debug_info: core.DebugInfo, *primals, **params):
  source_info = source_info_util.current()
  with core.take_current_trace() as parent_trace:
    tangent_trace = pe.DynamicJaxprTrace(debug_info, auto_dce=True)
    tangent_trace.tag = _tag
    linearize_trace = LinearizeTrace(parent_trace, tangent_trace, _is_vjp)
    tracers = [LinearizeTracer(linearize_trace, p,
                               tangent_trace.new_arg(typeof(p).to_tangent_aval(),
                                                     source_info))
               if nz else p
               for p, nz in zip(primals, nzs_in)]
    with core.set_current_trace(linearize_trace, check_leaks=True):
      ans = _f(*tracers)
      out_primals, out_tangents = unzip2(map(linearize_trace.to_primal_tangent_pair, ans))
      del linearize_trace, ans, tracers
  nzs_out = tuple(type(t) is not Zero for t in out_tangents)
  out_tangents = tuple(t for t, nz in zip(out_tangents, nzs_out) if nz)
  out_tangents = map(partial(tangent_trace.to_jaxpr_tracer, source_info=source_info),
                     out_tangents)
  jaxpr, consts = tangent_trace.to_jaxpr(
      out_tangents, debug_info.with_unknown_names(), source_info)
  which_env = [(isinstance(c, pe.DynamicJaxprTracer) and
                getattr(c._trace, 'tag', None) is _tag) for c in consts]
  jaxpr = pe.move_envvars(jaxpr, tuple(which_env))
  res, env = partition_list(which_env, consts)
  residual_avals = map(typeof, res)
  # Which residuals are just forwarded inputs? Check object id.
  id_map = {id(p): i for i, p in enumerate(primals)}
  in_fwd: list[int | None] = [id_map.get(id(r)) for r in res]
  # Which residuals are already primal outputs? Check object id.
  id_map = {id(p): i for i, p in enumerate(out_primals)}
  out_fwd: list[int | None] = [id_map.get(id(r)) for r in res]
  # Prune residuals not to include forwarded primal inputs or outputs.
  res = [p for p, f1, f2 in zip(res, in_fwd, out_fwd) if f1 is None and f2 is None]
  _store.store((residual_avals, nzs_out, jaxpr, env, in_fwd, out_fwd))
  return *res, *out_primals

