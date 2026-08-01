
def _dedup_consts(jaxpr, num_consts, const_ids):
  newvars = {}
  canonicalize = {v: newvars.setdefault(constid, v)
                  for constid, v in zip(const_ids, jaxpr.invars[:num_consts])}
  eqns = [e.replace(invars=[canonicalize.get(x, x) if isinstance(x, core.Var)
                            else x for x in e.invars],
                    effects=core.subst_input_effects(e.effects, canonicalize))
          for e in jaxpr.eqns]
  outvars = [canonicalize.get(x, x) if isinstance(x, core.Var) else x
             for x in jaxpr.outvars]
  invars = [*list(newvars.values()), *jaxpr.invars[num_consts:]]
  effs = core.subst_input_effects(jaxpr.effects, canonicalize)
  jaxpr = jaxpr.replace(jaxpr=jaxpr.jaxpr.replace(invars=invars, eqns=eqns, outvars=outvars,
                        effects=effs))
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  return jaxpr

