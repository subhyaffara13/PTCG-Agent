
def get_out_layouts_via_propagation(closed_jaxpr: core.ClosedJaxpr
                                    ) -> tuple[None | Layout]:
  env = {}
  jaxpr = closed_jaxpr.jaxpr

  def read(var):
    if type(var) is core.Literal:
      return None
    return env[var]

  def write(var, val):
    env[var] = val

  safe_map(write, jaxpr.invars, [None] * len(jaxpr.invars))
  safe_map(write, jaxpr.constvars, [None] * len(jaxpr.constvars))

  for eqn in jaxpr.eqns:
    if eqn.primitive is pjit.sharding_constraint_p:
      out_eqn_layouts = [eqn.params['layout']]
    elif eqn.primitive is pjit.layout_constraint_p:
      out_eqn_layouts = [eqn.params['layout']]
    else:
      out_eqn_layouts = [None] * len(eqn.outvars)
    safe_map(write, eqn.outvars, out_eqn_layouts)
  return tuple(safe_map(read, jaxpr.outvars))

