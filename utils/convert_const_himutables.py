
def convert_const_himutables(jaxpr):
  move = [typeof(c).has_qdd for c in jaxpr.consts]
  constvals, in_mutables = partition_list(move, jaxpr.consts)
  constvars, boxvars = partition_list(move, jaxpr.jaxpr.constvars)
  invars = *boxvars, *jaxpr.jaxpr.invars
  effects = make_jaxpr_effects(constvars, invars, jaxpr.jaxpr.outvars,
                               jaxpr.jaxpr.eqns)
  new_jaxpr = jaxpr.jaxpr.replace(constvars=constvars, invars=invars,
                                  effects=effects)
  return jaxpr.replace(jaxpr=new_jaxpr, consts=constvals), in_mutables

