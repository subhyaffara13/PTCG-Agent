
def _run_state_to_lojax(*args, jaxpr, is_initialized, **params):
  assert not jaxpr.constvars
  closed_jaxpr = core.ClosedJaxpr(jaxpr, ())
  arg_avals = map(core.typeof, args)
  lo_args, is_initialized = unzip2(
      (lo_val, is_init) for a, x, is_init in zip(arg_avals, args, is_initialized)
      for lo_val in (a.read_loval(x) if a.has_qdd else a.lower_val(x)))
  lo_jaxpr = pe.lower_jaxpr2(closed_jaxpr)
  lo_outs = run_state_p.bind(*lo_jaxpr.consts, *lo_args, jaxpr=lo_jaxpr.jaxpr,
                             is_initialized=is_initialized, **params)
  return pe.raise_lo_outs(arg_avals, lo_outs)

