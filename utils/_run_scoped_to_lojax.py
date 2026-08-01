
def _run_scoped_to_lojax(*args, jaxpr, **params):
  closed_hi_jaxpr = jax_core.ClosedJaxpr(jaxpr, args)
  closed_lo_jaxpr = pe.lower_jaxpr2(closed_hi_jaxpr)
  consts = closed_lo_jaxpr.consts
  return run_scoped_p.bind(*consts, jaxpr=closed_lo_jaxpr.jaxpr, **params)

