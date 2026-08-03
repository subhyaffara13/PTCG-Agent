from typing import Any

def physicalize_interp(
    jaxpr: core.Jaxpr, consts: Sequence[core.Value], *args: core.Value
):
  """Physicalizes a jaxpr by replacing fusible dtypes with physical types."""
  # TODO: Merge into JAX core.
  env: dict[core.Var, Any] = {}

  def read_env(var: core.Atom):
    if isinstance(var, core.Literal):
      return var.val
    return env[var]

  def write_env(var: core.Var, val: Any):
    env[var] = val

  foreach(write_env, jaxpr.constvars, consts)
  assert len(jaxpr.invars) == len(
      args
  ), f"Length mismatch: {jaxpr.invars} != {args}"
  foreach(write_env, jaxpr.invars, args)

  for eqn in jaxpr.eqns:
    invals = list(map(read_env, eqn.invars))
    avals_in = tuple(x.aval for x in eqn.invars)
    name_stack = (
        source_info_util.current_name_stack() + eqn.source_info.name_stack
    )
    with (
        source_info_util.user_context(
            eqn.source_info.traceback, name_stack=name_stack
        ),
        eqn.ctx.manager,
    ):
      # need to check types and then invoke the correct rule.
      ctx = Context(
          avals_in=avals_in, avals_out=[var.aval for var in eqn.outvars]
      )
      custom_rule = _phys_find_rule(eqn.primitive, avals_in)
      if custom_rule:
        outvals = custom_rule(ctx, *invals, **eqn.params)
      else:
        bind_params = eqn.primitive.get_bind_params(eqn.params)
        outvals = eqn.primitive.bind(*invals, **bind_params)

    if eqn.primitive.multiple_results:
      assert len(outvals) == len(eqn.outvars), eqn
      foreach(write_env, eqn.outvars, outvals)
    else:
      write_env(eqn.outvars[0], outvals)

  return map(read_env, jaxpr.outvars)

