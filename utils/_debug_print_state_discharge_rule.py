
def _debug_print_state_discharge_rule(in_avals, out_avals, *args, **kwargs):
  del in_avals, out_avals  # Unused.
  out = debug_print_p.bind(*args, **kwargs)
  return args, out

