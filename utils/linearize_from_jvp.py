
def linearize_from_jvp(jvp: lu.WrappedFun,
                       multiple_results: bool,
                       nonzeros: Sequence[bool],
                       user_facing_symbolic_zeros: bool, instantiate_input_zeros: bool,
                       primals, params):
  current_name_stack = source_info_util.current_name_stack()
  with core.take_current_trace() as parent_trace:
    trace = pe.JaxprTrace(parent_trace, current_name_stack, core.TraceTag())
    tangent_avals = [typeof(p).to_tangent_aval() for p in primals]

    # map tangents with float0 dtype to symbolic zeros
    nonzeros = [nz and not (isinstance(a, core.ShapedArray) and a.dtype == float0)
                for a, nz in zip(tangent_avals, nonzeros)]

    def make_zero(aval):
      if instantiate_input_zeros:
        return zeros_like_aval(aval)
      elif user_facing_symbolic_zeros:
        return SymbolicZero(aval)
      else:
        return Zero(aval)

    if user_facing_symbolic_zeros:
      zero_type = SymbolicZero
    else:
      zero_type = Zero

    with core.set_current_trace(trace):
      tangent_args = [trace.new_arg(pe.PartialVal.unknown(a)) if nz else make_zero(a)
                      for a, nz in zip(tangent_avals, nonzeros)]
      out_primals, out_tangents = jvp.call_wrapped(
          tuple(primals), tuple(tangent_args), **params)

    if not multiple_results:
      out_primals = [out_primals]
      out_tangents = [out_tangents]

    out_primals = [trace.to_jaxpr_tracer(p).pval.get_known() for p in out_primals]
    if any(p is None for p in out_primals):
      raise ValueError(
          "Linearization failed to produce known values for all output primals. "
          "This is typically caused by attempting to differentiate a function "
          "uses an operation that does not support reverse-mode autodiff.")

    out_nzs = [type(t) is not zero_type and not trace.to_jaxpr_tracer(t).is_known()
               for t in out_tangents]
    out_tangent_avals = [typeof(p).to_tangent_aval() for p in out_primals]
    out_nz_tracers = [trace.to_jaxpr_tracer(r)
                      for (r, nz) in zip(out_tangents, out_nzs) if nz]
    in_tracers = [t for t, nz in zip(tangent_args, nonzeros) if nz]
    jaxpr, out_consts, _ = pe.tracers_to_jaxpr(
        in_tracers, out_nz_tracers, trace.effect_handles,
        jvp.debug_info.with_unknown_names())
    jaxpr, used_consts, _ = pe.dce_jaxpr_consts(
        jaxpr, [True] * len(jaxpr.outvars),
        [False] * len(jaxpr.constvars) + [True] * len(jaxpr.invars))
    out_consts = [c for used, c in zip(used_consts, out_consts) if used]

    def linearized(residuals, *tangents):
      nz_tangents_in = [t for (t, nz) in zip(tangents, nonzeros) if nz]
      nz_tangents_out = core.eval_jaxpr(jaxpr, residuals, *nz_tangents_in)
      nz_tangents_out_iter = iter(nz_tangents_out)
      all_out_tangents = [next(nz_tangents_out_iter) if nz else Zero(aval)
                          for (aval, nz) in zip(out_tangent_avals, out_nzs)]
      if multiple_results:
        return all_out_tangents
      else:
        out_tangent, = all_out_tangents
        return out_tangent

  if multiple_results:
    return out_primals, out_nzs, out_consts, linearized
  else:
    out_primal, = out_primals
    out_nz, = out_nzs
    return out_primal, out_nz, out_consts, linearized

