
def _check_closed_call(_, *in_atoms, call_jaxpr):
  in_avals = [x.aval for x in in_atoms]
  if not all(map(typecompat, call_jaxpr.in_avals, in_avals)):
    raise JaxprTypeError("Closed call in_avals mismatch")
  return call_jaxpr.out_avals, positional_effects(call_jaxpr)

