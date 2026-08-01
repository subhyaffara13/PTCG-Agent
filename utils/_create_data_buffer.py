
def _create_data_buffer(
    np_array: np.ndarray,
    device: jax.Device,
    shard_size: int | None,
    shard_index: int,
) -> jax.Array:
  """Creates a data buffer for a device."""
  if shard_size is None:
    return jnp.expand_dims(jax.device_put(np_array, device), axis=0)
  else:
    shard_start = shard_index * shard_size
    shard_end = (shard_index + 1) * shard_size
    tensor_shard = np_array[shard_start:shard_end]
    return jnp.expand_dims(jax.device_put(tensor_shard, device), axis=0)

