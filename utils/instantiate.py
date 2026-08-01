
def instantiate(z: Zero | Array) -> Array:
  if isinstance(z, Zero):
    return zeros_like_aval(z.aval)
  return z

