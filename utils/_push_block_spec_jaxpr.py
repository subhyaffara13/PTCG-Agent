
def _push_block_spec_jaxpr(
    jaxpr: core.Jaxpr,
    *flat_block_specs,
) -> tuple[pallas_core.BlockSpec, ...]:
  num_inputs = len(jaxpr.invars)
  if len(flat_block_specs) != num_inputs:
    raise ValueError(
        f'Expected {num_inputs} block specs, got {len(flat_block_specs)}'
    )

  env: dict[core.Var, pallas_core.BlockSpec | pallas_core.NoBlockSpec] = {}

  for invar, bs in zip(jaxpr.invars, flat_block_specs, strict=True):
    env[invar] = bs
  for constvar in jaxpr.constvars:
    env[constvar] = pallas_core.no_block_spec

  def _read_block_spec(
      atom: core.Atom,
  ) -> pallas_core.BlockSpec | pallas_core.NoBlockSpec:
    if isinstance(atom, core.Literal):
      return pallas_core.no_block_spec
    return env[atom]

  def _write_block_spec(
      atom: core.Atom,
      block_spec: pallas_core.BlockSpec | pallas_core.NoBlockSpec,
  ):
    if isinstance(atom, core.Literal):
      return
    env[atom] = block_spec

  for eqn in jaxpr.eqns:
    in_block_specs = tuple(util.safe_map(_read_block_spec, eqn.invars))
    if all(bs is pallas_core.no_block_spec for bs in in_block_specs):
      for outvar in eqn.outvars:
        _write_block_spec(outvar, pallas_core.no_block_spec)
      continue
    rule = push_block_spec_rules.get(eqn.primitive, None)
    if not rule:
      raise NotImplementedError(eqn.primitive)
    ctx = PushRuleContext(
        avals_in=tuple(v.aval for v in eqn.invars),
        avals_out=tuple(v.aval for v in eqn.outvars),
    )
    if eqn.primitive.multiple_results:
      out_block_specs = rule(ctx, *in_block_specs, **eqn.params)
    else:
      out_block_specs = [rule(ctx, *in_block_specs, **eqn.params)]

    util.safe_map(_write_block_spec, eqn.outvars, out_block_specs)
  out_block_specs = tuple(util.safe_map(_read_block_spec, jaxpr.outvars))
  valid_block_spec = [
      bs for bs in flat_block_specs if bs is not pallas_core.no_block_spec
  ][0]
  out_block_specs = tuple(
      valid_block_spec if obs is pallas_core.no_block_spec else obs
      for obs in out_block_specs
  )
  if any(bs is pallas_core.no_block_spec for bs in out_block_specs):
    raise ValueError('No block spec found for output')
  return out_block_specs

