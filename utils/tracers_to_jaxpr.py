from typing import Any

def tracers_to_jaxpr(
  in_tracers: Sequence[JaxprTracer],
  out_tracers: Sequence[JaxprTracer],
  effect_handles: Sequence[Any],
  debug_info: core.DebugInfo,
  ) -> tuple[Jaxpr, tuple[Any, ...], tuple[Any, ...]]:
  """Constructs Jaxpr given tracers for inputs and outputs.

  Params:
    in_tracers: the tracers that were created for the function inputs
    out_tracers: the tracers that were output by the function.
    debug_info: the debug info for the function.

  Returns: a triple of a `Jaxpr`, a list of constant values corresponding to
    the `constvars` in the returned Jaxps, and a list of environment values.
    The vars for the environment values have been prepended to the Jaxpr's
    `invars`.
  """
  gensym = core.gensym()

  t_to_var: dict[TracerId, Var] = {}
  consts: dict[Var, Any] = {}
  env: dict[Var, JaxprTracer] = {}
  constid_to_var: dict[ConstId, Var] = {}  # for deduplication

  def get_atom(t: JaxprTracer) -> Atom:
    return t.recipe if type(t.recipe) is Literal else t_to_var[id(t)]

  def newvar(t: JaxprTracer | None) -> Var:
    assert t is not None
    var = gensym(t.aval)
    var_ = t_to_var.setdefault(id(t), var)
    assert var is var_
    return var

  processed_eqn_ids = set()
  eqns: list[core.JaxprEqn] = []
  is_high = False

  reachable = toposort
  tracers = reachable((*in_tracers, *out_tracers, *effect_handles))
  def sort_key(t):
    r = t.recipe
    return r.eqn_id if isinstance(r, JaxprEqnRecipe) else -1
  tracers = sorted(tracers, key=sort_key)

  for t in tracers:
    r = t.recipe
    if isinstance(r, JaxprEqnRecipe):
      # TODO broadcast_in_dim can create a new tracer, not present in parents
      if r.eqn_id not in processed_eqn_ids:
        in_atoms = map(get_atom, r.in_tracers)
        outvars = [DropVar(a) if rf() is None else newvar(rf())
                   for a, rf in zip(r.out_avals, r.out_tracer_refs)]
        eqns.append(new_jaxpr_eqn(in_atoms, outvars, r.primitive, r.params,
                                  r.effects, r.source_info, r.ctx))
        in_avals = [x.aval for x in in_atoms]
        is_high |= r.primitive.is_high(*in_avals, **r.params)
        processed_eqn_ids.add(r.eqn_id)
    elif isinstance(r, LambdaBinding):
      if not any(t is in_tracer for in_tracer in in_tracers):
        raise core.escaped_tracer_error(t, f"Tracer not in input tracers: {t}")
      newvar(t)
    elif isinstance(r, ConstVar):
      var = constid_to_var.get(id(r.val))
      if var is None:
        var = constid_to_var[id(r.val)] = newvar(t)
        consts[var] = r.val
      t_to_var[id(t)] = var
    elif isinstance(r, FreeVar):
      env[newvar(t)] = r.val
    elif isinstance(r, Literal):
      pass
    elif r is None:
      assert False
    else:
      raise TypeError(r)

  env_vars, env_vals = unzip2(env.items())
  invars = [*env_vars, *map(get_atom, in_tracers)]
  const_vars, const_vals = unzip2(consts.items())
  outvars = map(get_atom, out_tracers)
  jaxpr_effects = make_jaxpr_effects(const_vars, invars, outvars, eqns)
  is_high |= any(x.aval.is_high for x in it.chain(const_vars, invars, outvars))
  jaxpr = Jaxpr(const_vars, invars,  # pyrefly: ignore[bad-argument-type]
                outvars, eqns, jaxpr_effects, debug_info, is_high)
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  # del getvar  # needed to avoid cyclic-reference closure, apparently!
  return jaxpr, const_vals, env_vals

