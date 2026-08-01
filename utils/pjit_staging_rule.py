
def pjit_staging_rule(trace, source_info, *args, **params):
  if params["compiler_options_kvs"]:
    raise ValueError(
        '`compiler_options` can only be passed to top-level `jax.jit`. Got'
        f' compiler_options={dict(params["compiler_options_kvs"])} specified on'
        f' a nested jit with name: {params["name"]} and source info:'
        f' {source_info_util.summarize(source_info)}')
  # If we're inlining, no need to compute forwarding information; the inlined
  # computation will in effect forward things.
  if (params["inline"] and
      all(isinstance(i, UnspecifiedValue) for i in params["in_shardings"]) and
      all(isinstance(o, UnspecifiedValue) for o in params["out_shardings"]) and
      all(i is None for i in params["in_layouts"]) and
      all(o is None for o in params["out_layouts"])):
    jaxpr = params["jaxpr"]
    out = pe.inline_jaxpr_into_trace(
        trace, source_info, jaxpr.jaxpr, jaxpr.consts, *args)
    return [trace.to_jaxpr_tracer(x, source_info) for x in out]

  jaxpr = params['jaxpr']
  if any(isinstance(c, core.Ref) for c in jaxpr.consts):
    jaxpr, consts = pxla._move_mutable_consts(jaxpr)
    consts = [trace.new_const(c, source_info) for c in consts]
    in_shardings = (*params['in_shardings'],) + (UNSPECIFIED,) * len(consts)
    in_layouts = (*params['in_layouts'],) + (None,) * len(consts)
    donated_invars = (*params['donated_invars'],) + (False,) * len(consts)
    new_params = dict(params, jaxpr=jaxpr, in_shardings=in_shardings,
                      in_layouts=in_layouts, donated_invars=donated_invars)
    out_tracers = trace.default_process_primitive(
        jit_p, (*args, *consts), new_params, source_info=source_info)
  else:
    out_tracers = trace.default_process_primitive(
        jit_p, args, params, source_info=source_info)
    # TODO(mattjj): handle qdd in the presence of refs
    for v, x in zip(it.chain(jaxpr.constvars, jaxpr.invars), it.chain(jaxpr.consts, args)):
      if v.initial_qdd:
        assert core.cur_qdd(x) == v.initial_qdd
        x.aval_mutable_qdd.mutable_qdd.update(v.final_qdd)
  return out_tracers

