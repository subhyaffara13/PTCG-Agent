
def _create_shared_zero_buffers(
    max_shard_shape_per_dtype: dict[np.dtype, list[int]],
    local_devices: list[jax.Device],
) -> dict[tuple[jax.Device, np.dtype], jax.Array]:
  """Creates shared zero buffers on local devices."""
  zero_buffers = {}
  for dtype, max_shape in max_shard_shape_per_dtype.items():
    for d in local_devices:
      zero_buffers[(d, dtype)] = jnp.zeros(
          tuple(max_shape), dtype=dtype, device=d
      )
  return zero_buffers

