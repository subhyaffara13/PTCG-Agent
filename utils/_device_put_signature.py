
def _device_put_signature(eqn):
  num_vals = len(eqn.invars)
  return KeyReuseSignature(*(Forward(i, i) for i in range(num_vals)))

