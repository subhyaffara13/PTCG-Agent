
def move_envvars(jaxpr: Jaxpr, which: tuple[bool, ...]) -> Jaxpr:
  constvars, envvars = partition_list(which, jaxpr.constvars)
  return jaxpr.replace(constvars=constvars, invars=[*envvars, *jaxpr.invars])

