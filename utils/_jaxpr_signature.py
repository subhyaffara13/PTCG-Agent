
def _jaxpr_signature(jaxpr_obj):
  env = {}
  if isinstance(jaxpr_obj, core.ClosedJaxpr):
    jaxpr = jaxpr_obj.jaxpr
    for v, c in zip(jaxpr.constvars, jaxpr_obj.consts):
      env[v] = ('constval', _make_hashable(c))
  else:
    jaxpr = jaxpr_obj
    for i, v in enumerate(jaxpr.constvars):
      env[v] = ('constvar_idx', i)
  for i, v in enumerate(jaxpr.invars):
    env[v] = ('invar', i)

  def get_var_sig(v):
    if isinstance(v, core.Literal):
      return ('literal', _make_hashable(v.val))
    elif type(v).__name__ == 'DropVar':
      return ('dropvar',)
    elif v in env:
      return env[v]
    else:
      return ('unknown_var', str(v))

  def get_effect_sig(e):
    if isinstance(e, effects_lib.JaxprInputEffect) and isinstance(
        e.input, core.Var):
      return f'{type(e).__name__}<{get_var_sig(e.input)}>'
    return str(e)

  eqn_sigs = []
  for eqn in jaxpr.eqns:
    in_sigs = tuple(hash(get_var_sig(v)) for v in eqn.invars)
    params_sig = hash(_make_hashable(eqn.params))
    effects = tuple(sorted(get_effect_sig(e) for e in getattr(eqn, 'effects', [])))
    op_sig = ('eqn', eqn.primitive.name, in_sigs, params_sig, effects)
    eqn_sigs.append(op_sig)
    for i, outvar in enumerate(eqn.outvars):
      if type(outvar).__name__ != 'DropVar':
        env[outvar] = ('out', op_sig, i)  # pyrefly: ignore[unsupported-operation]
  out_sigs = tuple(get_var_sig(v) for v in jaxpr.outvars)
  jaxpr_effects = tuple(
      sorted(get_effect_sig(e) for e in getattr(jaxpr, 'effects', [])))
  eqn_sigs_sorted = tuple(sorted(eqn_sigs, key=lambda x: str(x)))
  return ('jaxpr_dag', out_sigs, eqn_sigs_sorted, jaxpr_effects)

