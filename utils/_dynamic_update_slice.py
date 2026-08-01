
def _dynamic_update_slice(start_idx, block_shape, value, update, is_squeeze):
  start_idx = tuple(jnp.asarray(s, dtype=jnp.int32) for s in start_idx)
  broadcast_dims = tuple(i for i, b in enumerate(is_squeeze)
                         if not b)
  update = lax.broadcast_in_dim(update, block_shape, broadcast_dims)
  assert update.shape == block_shape
  return slicing.dynamic_update_slice(value, update, start_idx)

