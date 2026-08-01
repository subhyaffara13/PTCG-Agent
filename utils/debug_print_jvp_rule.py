
def debug_print_jvp_rule(primals, tangents, **params):
  return debug_print_p.bind(*primals, **params), []

