
def _vdot_safe(a, b):
  return _vdot(jnp.asarray(a), jnp.asarray(b))

