
def _inspect_sharding_jvp_rule(primals, _, **params):
  return inspect_sharding_p.bind(*primals, **params), []

