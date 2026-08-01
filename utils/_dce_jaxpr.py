
def _dce_jaxpr(jaxpr: Jaxpr, used_outputs: tuple[bool, ...],
               instantiate: tuple[bool, ...]
               ) -> tuple[Jaxpr, list[bool]]:
  env: dict[Var, bool] = {}

  def read(v: Var) -> bool:
    return env.get(v, False)

  def write(x: Atom, b: bool) -> None:
    if type(x) is Var:
      env[x] = read(x) or b

  new_eqns = []
  foreach(write, jaxpr.outvars, used_outputs)
  for eqn in jaxpr.eqns[::-1]:
    used_outs = map(read, eqn.outvars)
    rule = dce_rules.get(eqn.primitive, _default_dce_rule)
    used_ins, new_eqn = rule(used_outs, eqn)
    if new_eqn is not None:
      new_eqns.append(new_eqn)
    foreach(write, eqn.invars, used_ins)
  used_inputs = map(read, jaxpr.invars)
  used_inputs = map(op.or_, instantiate, used_inputs)

  invars = [v for v, b in zip(jaxpr.invars, used_inputs)   if b]
  outvars = [v for v, b in zip(jaxpr.outvars, used_outputs) if b]
  eqns = new_eqns[::-1]
  jaxpr_effects = make_jaxpr_effects(jaxpr.constvars, invars, outvars, eqns)

  dbg = core.DebugInfo(
      jaxpr.debug_info.traced_for, jaxpr.debug_info.func_src_info,
      jaxpr.debug_info.filter_arg_names(used_inputs),
      jaxpr.debug_info.filter_result_paths(used_outputs))
  new_jaxpr = jaxpr.replace(invars=invars, outvars=outvars, eqns=eqns,
                            effects=jaxpr_effects, debug_info=dbg)
  config.enable_checks.value and core.check_jaxpr(new_jaxpr)

  return new_jaxpr, used_inputs


def _dce_jaxpr(closed_jaxpr, keep_unused, donated_invars):
  assert isinstance(closed_jaxpr, core.ClosedJaxpr)
  jaxpr = closed_jaxpr.jaxpr
  consts = closed_jaxpr.consts
  in_avals = closed_jaxpr.in_avals

  if (keep_unused or any(hasattr(a, "shape") and not core.is_constant_shape(a.shape)
                         for a in in_avals)):
    kept_var_idx = set(range(len(in_avals)))
  else:
    jaxpr, kept_const_idx, kept_var_idx = prune_unused_inputs(jaxpr)
    consts = [c for i, c in enumerate(consts) if i in kept_const_idx]
    donated_invars = tuple(x for i, x in enumerate(donated_invars) if i in kept_var_idx)
    del kept_const_idx

  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  return closed_jaxpr, donated_invars, kept_var_idx

