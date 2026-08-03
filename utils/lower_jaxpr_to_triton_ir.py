from typing import Any

def lower_jaxpr_to_triton_ir(
    ctx: ModuleContext,
    jaxpr: jax_core.Jaxpr,
    block_infos: Sequence[BlockInfo | None] | None,
    *args,
) -> Sequence[Any]:
  env = {}
  block_info_env = {}

  def read_env(atom: jax_core.Atom):
    return atom.val if isinstance(atom, jax_core.Literal) else env[atom]

  def read_block_info_env(atom: jax_core.Atom):
    if isinstance(atom, jax_core.Literal):
      return None
    return block_info_env.get(atom)

  def write_env(var: jax_core.Var, val):
    env[var] = val

  if block_infos is not None:
    for invar, block_info in zip(jaxpr.invars, block_infos):
      if block_info is not None:
        block_info_env[invar] = block_info

  foreach(write_env, jaxpr.invars, args)

  for eqn in jaxpr.eqns:
    invals = map(read_env, eqn.invars)
    if eqn.primitive not in triton_lowering_rules:
      raise NotImplementedError(
          "Unimplemented primitive in Pallas Triton lowering:"
          f" {eqn.primitive.name}. Please file an issue at"
          " https://github.com/jax-ml/jax/issues/new/choose."
      )
    rule = triton_lowering_rules[eqn.primitive]
    avals_in = [v.aval for v in eqn.invars]
    avals_out = [v.aval for v in eqn.outvars]
    eqn_block_infos = map(read_block_info_env, eqn.invars)
    loc = mlir.source_info_to_location(
        ctx, eqn.primitive, eqn.source_info.name_stack,
        eqn.source_info.traceback)
    rule_ctx = LoweringRuleContext(ctx, avals_in, avals_out, eqn_block_infos)  # pyrefly: ignore[bad-argument-type]  # pyrefly#2385
    try:
      with source_info_util.user_context(eqn.source_info.traceback), loc:
        outvals: Any = rule(rule_ctx, *invals, **eqn.params)
    except LoweringError:
      raise  # We only add the extra info to the innermost exception.
    except Exception as e:
      if not config.jax_pallas_verbose_errors.value:
        raise
      inval_types = map(lambda t: getattr(t, "type", None), invals)
      raise LoweringError(
          f"Exception while lowering eqn:\n  {eqn}\nWith context:\n "
          f" {rule_ctx}\nWith inval types={inval_types}\nIn jaxpr:\n{jaxpr}\n"
          f"msg={e}"
      ) from e
    if eqn.primitive.multiple_results:
      if len(eqn.outvars) != len(outvals):
        raise ValueError(
            f"Primitive {eqn.primitive.name} has multiple results, but "
            f"{len(eqn.outvars)} outvars do not match {len(outvals)} outvals."
        )
      foreach(write_env, eqn.outvars, outvals)
    else:
      write_env(eqn.outvars[0], outvals)

  return map(read_env, jaxpr.outvars)

