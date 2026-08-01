
def _remat_opt_abstract_eval(*args, fwd_jaxpr: core.ClosedJaxpr, **_):
  del args
  return fwd_jaxpr.out_avals, core.positional_effects(fwd_jaxpr)

