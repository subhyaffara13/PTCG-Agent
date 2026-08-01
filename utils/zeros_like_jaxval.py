
def zeros_like_jaxval(val):
  return zeros_like_aval(core.typeof(val))

