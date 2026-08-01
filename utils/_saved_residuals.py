
def _saved_residuals(jaxpr: core.Jaxpr,
                     arg_names: Sequence[str]) -> list[tuple[core.AbstractValue, str]]:
  res_lits = [x for x in jaxpr.outvars if     isinstance(x, core.Literal)]
  res_vars = {x for x in jaxpr.outvars if not isinstance(x, core.Literal)}

  # don't count reduce_precision_p as the producer, look through it instead
  subst = {e.outvars[0]: e.invars[0] for e in jaxpr.eqns
           if e.primitive is lax_internal.reduce_precision_p}
  res_vars = {subst.get(v, v) for v in res_vars}

  results = []

  for x in res_lits:
    results.append((x.aval, 'from a literal'))

  for v in jaxpr.constvars:
    if v in res_vars:
      results.append((v.aval, 'from a constant'))

  for i, v in enumerate(jaxpr.invars):
    if v in res_vars:
      if arg_names[i]:
        src = f'from the argument {arg_names[i]}'
      else:
        src = 'from the argument at flattened index {i}'
      results.append((v.aval, src))

  def get_name(eqn) -> str | None:
    if eqn.primitive is name_p:
      return eqn.params['name']
    elif (eqn.primitive is call_hi_primitive_p
          and isinstance(p := eqn.params['_prim'], CheckpointName)):
      return p.name

  # TODO(mattjj): actually we want to flag this case as problematic, ie some
  # other consumer of the input to a name_p
  # named_vars = {v: e for e in jaxpr.eqns if e.primitive is name_p
  #               for v in e.invars}

  for eqn in jaxpr.eqns:
    for v in eqn.outvars:
      if v in res_vars:
        src = source_info_util.summarize(eqn.source_info)
        if name := get_name(eqn):
          results.append((v.aval, f"named '{name}' from {src}"))
        elif eqn.primitive.name == 'jit':
          results.append((v.aval,
                          f"output of jitted function '{eqn.params['name']}' "
                          f"from {src}"))
        else:
          results.append((v.aval, f'output of {eqn.primitive.name} from {src}'))

  assert len(results) == len(jaxpr.outvars)
  return results

