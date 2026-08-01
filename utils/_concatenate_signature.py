
def _concatenate_signature(eqn):
  num_vals = len(eqn.invars)
  # TODO(jakevdp): should this signature be more granular?
  if num_vals == 1:
    return KeyReuseSignature(Forward(0, 0))
  else:
    return KeyReuseSignature(*(Sink(i) for i in range(num_vals)), Source(0))

