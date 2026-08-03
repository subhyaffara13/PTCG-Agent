from typing import Any

def create_value_metadata(value: Any) -> Any:
  """Creates Metadata for the given value matching Orbax's return type."""
  if isinstance(value, jax.Array):
    sharding_metadata_obj = sharding_metadata.from_jax_sharding(value.sharding)
    storage_metadata = value_metadata.StorageMetadata(
        chunk_shape=value.sharding.shard_shape(value.shape),
        write_shape=value.shape,
    )
    return array_leaf_handler.ArrayMetadata(
        shape=value.shape,
        dtype=jnp.dtype(value.dtype),
        sharding_metadata=sharding_metadata_obj,
        storage_metadata=storage_metadata,
    )
  elif isinstance(value, (int, np.integer)):
    return 0
  elif isinstance(value, (float, np.floating)):
    return 0.0
  else:
    raise TypeError(f'Unsupported type: {type(value)}')

