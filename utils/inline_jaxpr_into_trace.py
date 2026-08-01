
def inline_jaxpr_into_trace(
    trace: DynamicJaxprTrace, src: SourceInfo, jaxpr: Jaxpr,
    consts: Sequence[Any], *arg_tracers: DynamicJaxprTracer) -> list[Any]:
  # This function is conceptually the same thing as just calling eval_jaxpr,
  const_tracers = map(partial(trace.new_const, source_info=src), consts)
  env: dict[Var, DynamicJaxprTracer] = dict(
      zip([*jaxpr.constvars, *jaxpr.invars],
          [*const_tracers, *arg_tracers]))

  def inline_atom(src_, x):
    if isinstance(x, Literal):
      return DynamicJaxprTracer(trace, x.aval, x, src_)
    else:
      return env[x]

  for eqn in jaxpr.eqns:
    src_ = (src if not eqn.source_info.name_stack else
            src.replace(name_stack=src.name_stack + eqn.source_info.name_stack))
    in_tracers = map(partial(inline_atom, src_), eqn.invars)
    out_avals = [v.aval for v in eqn.outvars]

    maybe_consts = try_constant_folding(eqn.primitive, in_tracers, eqn.params, out_avals)
    if maybe_consts is not None:
      out_tracers = [trace.new_const(c, source_info=src_, aval=aval)
                     for c, aval in zip(maybe_consts, out_avals)]
    else:
      effs = {e.replace(env[e.input].val)
              if isinstance(e, effects.JaxprInputEffect) else e
              for e in eqn.effects} if eqn.effects else eqn.effects
      out_tracers = trace.emit_eqn(in_tracers, out_avals, eqn.primitive,
                                   eqn.params, effs, src_, eqn.ctx)
    foreach(env.setdefault, eqn.outvars, out_tracers)

  return map(partial(inline_atom, src), jaxpr.outvars)

