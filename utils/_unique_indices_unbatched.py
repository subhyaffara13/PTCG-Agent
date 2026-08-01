
def _unique_indices_unbatched(indices, *, shape, return_inverse=False,
                              return_index=False, return_true_size=False):
  props = _validate_bcoo_indices(indices, shape)
  if props.n_sparse == 0:
    nse = 1
    indices_out = jnp.zeros_like(indices, shape=(nse, 0))
    out = (indices_out,)
    if return_index:
      out = (*out, jnp.zeros(nse, dtype='int32'))
    if return_inverse:
      out = (*out, jnp.zeros(nse, dtype='int32'))
    if return_true_size:
      out = (*out, nse)
    return out[0] if len(out) == 1 else out
  fill_value = jnp.expand_dims(jnp.array(shape[:props.n_sparse], dtype=indices.dtype), (0,))
  out_of_bounds = (indices >= fill_value).any(-1, keepdims=True)
  indices = jnp.where(out_of_bounds, fill_value, indices)
  # TODO: check if `indices_sorted` is True.
  out = _unique(indices, axis=0, return_inverse=return_inverse, return_index=return_index,
                return_true_size=return_true_size, size=props.nse, fill_value=fill_value)
  if return_inverse:
    idx = 2 if return_index else 1
    out = (*out[:idx], out[idx].ravel(), *out[idx + 1:])
  if return_true_size:
    nse = out[-1]
    nse = nse - (indices == fill_value).any().astype(nse.dtype)
    out = (*out[:-1], nse)
  return out

