
def _pad_in_dim(x, low=0, high=0, interior=0, fill_value=0, axis=0):
  pads = [(0, 0, 0)] * x.ndim
  pads[axis] = (low, high, interior)
  return lax.pad(x, jnp.array(fill_value, x.dtype), pads)

