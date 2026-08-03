import functools
from typing import Any

def checkify_jaxpr_flat(jaxpr: core.Jaxpr, consts: Sequence[core.Value],
                        enabled_errors, err_tree: PyTreeDef,
                        *args: core.Value) -> tuple[Error, list[Any]]:
  env: dict[core.Var, Any] = {}
  err_vals, in_args = split_list(args, [err_tree.num_leaves])
  error = jtu.tree_unflatten(err_tree, err_vals)

  last_used = core.last_used(jaxpr)

  def read_env(var: core.Atom):
    if isinstance(var, core.Literal):
      return var.val
    return env[var]

  def write_env(var: core.Var, val: Any):
    env[var] = val

  foreach(write_env, jaxpr.constvars, consts)
  foreach(write_env, jaxpr.invars, in_args)

  # interpreter loop
  for eqn in jaxpr.eqns:
    invals = map(read_env, eqn.invars)
    checkify_rule = error_checks.get(
        eqn.primitive, functools.partial(default_checkify_rule, eqn.primitive))
    name_stack = source_info_util.current_name_stack() + eqn.source_info.name_stack
    with (source_info_util.user_context(eqn.source_info.traceback,
                                        name_stack=name_stack),
          eqn.ctx.manager):
      error, outvals = checkify_rule(error, enabled_errors,
                                     *invals, **eqn.params)
    if eqn.primitive.multiple_results:
      foreach(write_env, eqn.outvars, outvals)
    else:
      write_env(eqn.outvars[0], outvals)
    core.clean_up_dead_vars(eqn, env, last_used)

  return error, map(read_env, jaxpr.outvars)

