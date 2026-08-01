
def _pad_constvars(jaxpr: core.ClosedJaxpr, num_consts: int,
                   left: tuple[core.AvalQDD, ...],
                   right: tuple[core.AbstractValue, ...]) -> core.ClosedJaxpr:
  def make_var(aq):
    return core.Var(aq.aval, initial_qdd=aq.qdd, final_qdd=aq.qdd)
  invars = [*map(make_var, left), *jaxpr.invars[:num_consts],
            *map(make_var, right), *jaxpr.invars[num_consts:]]
  jaxpr = jaxpr.replace(jaxpr=jaxpr.jaxpr.replace(invars=invars))
  config.enable_checks.value and core.check_jaxpr(jaxpr.jaxpr)
  return jaxpr

