
def convert_constvars_jaxpr(jaxpr: Jaxpr) -> Jaxpr:
  """Moves the constvars to the start of invars."""
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  if jaxpr.debug_info.arg_names is None:
    arg_names = None
  else:
    arg_names = ("",) * len(jaxpr.constvars) + (*jaxpr.debug_info.arg_names,)
  dbg = jaxpr.debug_info._replace(arg_names=arg_names)
  lifted_jaxpr = jaxpr.replace(
      constvars=(), invars=jaxpr.constvars + jaxpr.invars, debug_info=dbg)
  config.enable_checks.value and core.check_jaxpr(lifted_jaxpr)
  return lifted_jaxpr

