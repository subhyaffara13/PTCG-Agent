
def _adjust_indices_nse(indices, *, nse, shape):
  props = _validate_bcoo_indices(indices, shape)
  if nse <= props.nse:
    indices = indices[..., :nse, :]
  else:
    fill = lax.broadcast_in_dim(
      operand=jnp.array(shape[props.n_batch:props.n_batch + props.n_sparse], dtype=indices.dtype),
      shape=(*indices.shape[:-2], nse - props.nse, indices.shape[-1]),
      broadcast_dimensions=(indices.ndim - 1,)
    )
    indices = lax.concatenate([indices, fill], dimension=indices.ndim - 2)
  return indices

