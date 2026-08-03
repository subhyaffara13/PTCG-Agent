from typing import Any, Callable

def eval_jaxpr_recursive(
    jaxpr: jax_core.Jaxpr,
    consts,
    *args,
    recurse_hop_rule: Callable[[jax_core.Jaxpr, Sequence[Any]],
                               tuple[jax_core.Jaxpr, Sequence[Any]]],
    propagate_source_info=True) -> list[Any]:
  """Evaluates a Jaxpr with recursion into higher-order primitives.

  ``recurse_hop_rule`` is a Jaxpr interpreter (translates a Jaxpr to a new
  Jaxpr) that will be called on sub-jaxprs of higher-order primitives, such
  as the body of a loop or branches of a conditional.

  Args:
    jaxpr: The Jaxpr to evaluate.
    consts: Consts that ``jaxpr`` closes over.
    *args: Input arguments to the ``jaxpr``.
    recurse_hop_rule: A Jaxpr interpreter to call on sub-jaxprs of
      higher-order primitives.
    propagate_source_info: Whether to propagate source info.
  """
  def read(v: jax_core.Atom) -> Any:
    return v.val if isinstance(v, jax_core.Literal) else env[v]

  def write(v: jax_core.Var, val: Any) -> None:
    env[v] = val

  env: dict[jax_core.Var, Any] = {}
  foreach(write, jaxpr.constvars, consts)
  foreach(write, jaxpr.invars, args)
  lu = jax_core.last_used(jaxpr)
  for eqn in jaxpr.eqns:
    in_vals = map(read, eqn.invars)
    name_stack = source_info_util.current_name_stack()
    name_stack += eqn.source_info.name_stack
    traceback = eqn.source_info.traceback if propagate_source_info else None
    with source_info_util.user_context(
        traceback, name_stack=name_stack), eqn.ctx.manager:
      if eqn.primitive in _eval_jaxpr_hop_rules:
        ans = _eval_jaxpr_hop_rules[eqn.primitive](
            recurse_hop_rule, *in_vals, **eqn.params)
      else:
        bind_params = eqn.primitive.get_bind_params(eqn.params)
        ans = eqn.primitive.bind(*in_vals, **bind_params)
    if eqn.primitive.multiple_results:
      foreach(write, eqn.outvars, ans)
    else:
      write(eqn.outvars[0], ans)
    jax_core.clean_up_dead_vars(eqn, env, lu)
  return map(read, jaxpr.outvars)

