
def convert_invars_to_constvars(jaxpr: Jaxpr, n: int) -> Jaxpr:
  """Move n invars to constvars. Like an inverse of convert_constvars_jaxpr."""
  if n == 0:
    return jaxpr.replace()  # 'return jaxpr' would create cache reference cycle
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  constvars, invars = split_list(jaxpr.invars, [n])
  if jaxpr.debug_info.arg_names is None:
    dbg = jaxpr.debug_info
  else:
    dbg = jaxpr.debug_info._replace(
        arg_names=jaxpr.debug_info.arg_names[n:])
  lifted_jaxpr = jaxpr.replace(constvars=tuple(constvars), invars=invars,
                               debug_info=dbg)
  config.enable_checks.value and core.check_jaxpr(lifted_jaxpr)
  return lifted_jaxpr

