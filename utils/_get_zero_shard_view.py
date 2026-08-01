
def _get_zero_shard_view(
    zero_buf: jax.Array, current_shard_shape: tuple[int, ...]
) -> jax.Array:
  """Returns a view of the shared zero buffer for a non-owner shard."""
  slices = [slice(0, 1)]
  for s_size in current_shard_shape[1:]:
    slices.append(slice(0, s_size))

  # Pad with 0 for remaining dimensions to reduce rank if needed.
  while len(slices) < len(zero_buf.shape):
    slices.append(0)

  return zero_buf[tuple(slices)]

