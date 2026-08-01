
def _tf_or_xnp(x: Array['*d']):
  xnp = lazy.get_xnp(x)
  if lazy.has_tf and xnp is lazy.tnp:
    return lazy.tf
  else:
    return xnp

