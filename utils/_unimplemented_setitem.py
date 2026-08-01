
def _unimplemented_setitem(self, i, x):
  msg = ("JAX arrays are immutable and do not support in-place item assignment."
         " Instead of x[idx] = y, use x = x.at[idx].set(y) or another .at[] method:"
         " https://docs.jax.dev/en/latest/_autosummary/jax.numpy.ndarray.at.html")
  raise TypeError(msg)

