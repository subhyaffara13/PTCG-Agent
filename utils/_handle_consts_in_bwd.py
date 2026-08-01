
def _handle_consts_in_bwd(f, const_avals, *args):
  return [Zero(a) for a in const_avals] + list(f(*args))

