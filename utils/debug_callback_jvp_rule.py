
def debug_callback_jvp_rule(primals, tangents, **params):
  return debug_callback_p.bind(*primals, **params), []

