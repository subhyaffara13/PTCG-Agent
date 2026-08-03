from typing import Any

def pad_jaxpr_constvars(jaxpr: jax_core.Jaxpr,
                        i: int,
                        all_const_avals: Sequence[Any]
                        ) -> jax_core.ClosedJaxpr:
  """Pads a Jaxpr with constvars from all branches.

  For primitives that have multiple Jaxprs (e.g. cond_p), we need
  to pad each Jaxpr with all consts from all branches so the
  signatures match, but only use the consts for this branch.
  """
  unused_const_vars = [tuple(map(jax_core.Var, const_avals))
                       for const_avals in all_const_avals]
  const_prefix = util.concatenate(unused_const_vars[:i])
  const_suffix = util.concatenate(unused_const_vars[i + 1:])
  constvars = [*const_prefix, *jaxpr.constvars, *const_suffix]
  jaxpr = jaxpr.replace(constvars=constvars)
  effects = pe.make_jaxpr_effects(jaxpr.constvars, jaxpr.invars,
                                  jaxpr.outvars, jaxpr.eqns)
  jaxpr = jaxpr.replace(effects=effects)
  return jax_core.ClosedJaxpr(pe.convert_constvars_jaxpr(jaxpr), ())

