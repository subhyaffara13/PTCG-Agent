
def lower_jaxpr(hi_jaxpr: ClosedJaxpr, lo_avals) -> tuple[ClosedJaxpr, FlatTree]:
  env: dict[Var, DynamicJaxprTracer | HTLV] = {}  # noqa # type:ignore

  parent_trace = core.trace_ctx.trace
  trace = DynamicJaxprTrace(hi_jaxpr.jaxpr.debug_info.with_unknown_names(),
                            parent_trace=parent_trace, lower=True)

  def read(src, x):
    if isinstance(x, Literal):
      return x.val
    elif (htlv := env.get(x)) is not None:  # noqa
      return htlv
    else:
      assert not x.aval.is_high
      return trace.var_to_tracer(x, src)  # noqa

  with (core.ensure_no_leaks(trace), source_info_util.reset_name_stack(),
        TracebackScope()):
    src = source_info_util.current()
    invals = outs = None

    lo_avals_lol, () = lo_avals.unflatten()
    for v, xs in zip(hi_jaxpr.invars, lo_avals_lol):
      if v.aval.is_high:
        xs = [trace.new_arg(x, source_info=src) for x in xs]
        if v.aval.has_qdd:
          env[v] = v.aval.new_from_loval(v.initial_qdd, *xs)
        else:
          env[v] = v.aval.raise_val(*xs)
      else:
        trace.frame.invars.append(v)

    for v, c in zip(hi_jaxpr.constvars, hi_jaxpr.consts):
      if v.aval.is_high:
        if v.aval.has_qdd: raise NotImplementedError
        env[v] = c
      else:
        tracer = DynamicJaxprTracer(trace, v.aval, v, src)
        trace.frame.constid_to_tracer[id(c)] = tracer
        trace.frame.constvar_to_val[v] = c

    with core.set_current_trace(trace):
      eqns = trace.frame.tracing_eqns
      for eqn in hi_jaxpr.eqns:
        maybe_invals = [env.get(x) if isinstance(x, Var) else None for x in eqn.invars]
        hi = eqn.primitive.is_high(*[v.aval for v in eqn.invars], **eqn.params)
        if all(x is None for x in maybe_invals) and not hi:
          eqns.append(eqn)
        elif not hi:
          new_invars = [x if isinstance(x, Literal) else
                        t.val if (t := env.get(x)) is not None else x
                        for x in eqn.invars]
          eqns.append(eqn.replace(invars=new_invars))
        else:
          invals = map(partial(read, eqn.source_info), eqn.invars)
          name_stack = source_info_util.current_name_stack() + eqn.source_info.name_stack
          with (source_info_util.user_context(eqn.source_info.traceback, name_stack=name_stack),
                eqn.ctx.manager):
            outs = eqn.primitive.to_lojax(*invals, **eqn.params)
          if eqn.primitive.multiple_results:
            foreach(env.setdefault, eqn.outvars, outs)
          else:
            env[eqn.outvars[0]] = outs

    tracer = partial(trace.to_jaxpr_tracer, source_info=src)
    fu = FlatTree.flatten(())
    out_mut = [v.aval.read_loval_out(v.final_qdd, env[v]).map(tracer)
               if v.aval.has_qdd else fu for v in hi_jaxpr.invars]
    out_tracers = [dtypes.canonicalize_value(read(src, x)) for x in hi_jaxpr.outvars]
    out_tracers = [v.aval.lower_val2(hi_val).map(tracer)
                  for v, hi_val in zip(hi_jaxpr.outvars, out_tracers)]
    out_tracers = FlatTree.pack((tuple(out_mut), tuple(out_tracers)))
    out_avals = out_tracers.map(typeof)
    dbg = _lower_debug_info(hi_jaxpr, out_mut)
    jaxpr, consts = trace.frame.to_jaxpr(trace, list(out_tracers), dbg, src)
    del trace, env, out_tracers, out_mut, tracer, read, outs, invals, eqns

  config.enable_checks.value and core.check_jaxpr(jaxpr)
  assert not any(v.aval.is_high for v in it.chain(jaxpr.constvars, jaxpr.invars))
  return ClosedJaxpr(jaxpr, consts), out_avals

