
def _cpu_repeat(array, *, repeats, axis):
  return jnp.repeat(array, repeats, axis=axis)

