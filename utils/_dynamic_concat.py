
def _dynamic_concat(a, b, m, axis=0):
  "Concatenates padded arrays `a` and `b` where the true size of `a` is `m`."
  if m is None:
    return jnp.concatenate([a, b], axis=axis)
  return lax.dynamic_update_slice_in_dim(
      _pad_in_dim(a, high=b.shape[axis], axis=axis), b, m, axis)

