
def _remat_opt_to_lojax(*hi_args, fwd_jaxpr: core.ClosedJaxpr, num_consts, **params):
  return _lower_and_eval("remat_opt", fwd_jaxpr, hi_args)

