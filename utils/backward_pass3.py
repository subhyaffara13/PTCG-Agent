
def backward_pass3(
    jaxpr: core.Jaxpr, transform_stack: bool,
    consts: Sequence[Array], primals_in: Sequence[Array | Ref | GradAccum],
    cotangents_in: Sequence[Array]) -> None:
  if all(type(ct) is Zero for ct in cotangents_in) and not jaxpr.effects:
    return

  env: dict = dict(zip((*jaxpr.constvars, *jaxpr.invars),
                       (*consts, *primals_in)))

  def read(x: core.Atom) -> Array | GradAccum:
    return x.val if isinstance(x, Literal) else env[x]

  lin_eqns = []
  for eqn in jaxpr.eqns:
    # TODO(mattjj): shorten the lifetime of the reference accumulators
    if eqn.primitive.ref_primitive:
      v, = eqn.outvars
      lin_eqns.append(eqn)
      if eqn.primitive is core.ref_p or eqn.primitive is core.empty_ref_p:
        env[v] = RefAccum(v.aval.inner_aval.to_ct_aval())  # type: ignore
      elif eqn.primitive is core.freeze_p:
        env[v] = ValAccum(v.aval.to_ct_aval())
      elif eqn.primitive is core.accum_grad_in_ref_p:
        env[v] = RefAccum(v.aval.to_ct_aval())
      else:
        assert False
    elif any(isinstance(read(x), GradAccum) for x in eqn.invars):
      for v in eqn.outvars:
        env[v] = ValAccum(v.aval.to_ct_aval())
      lin_eqns.append(eqn)
    else:
      params = eqn.primitive.get_bind_params(eqn.params)
      with eqn.ctx.manager, _name_stack_ctx(eqn.source_info):
        ans = eqn.primitive.bind(*map(read, eqn.invars), **params)
      ans = ans if eqn.primitive.multiple_results else [ans]
      foreach(env.setdefault, eqn.outvars, ans)

  ctx = (source_info_util.transform_name_stack('transpose') if transform_stack
         else contextlib.nullcontext())
  for acc, ct in zip(map(read, jaxpr.outvars), cotangents_in):
    if isinstance(acc, GradAccum):
      acc.accum(ct)  # jaxpr.outvars can have Literals, env can have inst zeros
  with ctx:
    for eqn in lin_eqns[::-1]:
      with eqn.ctx.manager, _name_stack_ctx(eqn.source_info):
        if eqn.primitive is core.empty_ref_p:
          env.pop(eqn.outvars[0]).freeze()
        elif eqn.primitive.ref_primitive:
          ct = env.pop(eqn.outvars[0]).freeze()
          acc = read(eqn.invars[0])
          if isinstance(acc, GradAccum):
            acc.accum(ct)
        else:
          cts_in = [env.pop(v).freeze() for v in eqn.outvars]
          if not eqn.primitive.multiple_results:
            cts_in, = cts_in
          if eqn.primitive in fancy_transposes:
            rule = fancy_transposes[eqn.primitive]
            rule(cts_in, *map(read, eqn.invars), **eqn.params)
          else:
            rule = get_primitive_transpose(eqn.primitive)
            primals = map(read, eqn.invars)
            up = lambda x: UndefinedPrimal(x.aval) if isinstance(x, GradAccum) else x
            if eqn.primitive.call_primitive:
              # TODO(mattjj,dougalm): remove this path by revising call/map trans
              cts_in_avals = [v.aval for v in eqn.outvars]
              params = dict(eqn.params)
              call_jaxpr = params.pop('call_jaxpr')
              cts_out = rule(params, call_jaxpr, map(up, primals), cts_in, cts_in_avals)
            else:
              cts_out = rule(cts_in, *map(up, primals), **eqn.params)
            for x, ct in zip(primals, cts_out):
              if isinstance(x, GradAccum):
                x.accum(ct)

