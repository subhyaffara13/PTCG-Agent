import logging
from typing import Optional

def from_jax_sharding(jax_sharding) -> Optional[ShardingMetadata]:
  """Converts `jax.sharding.Sharding` to `ShardingMetadata`."""
  if isinstance(jax_sharding, jax.sharding.NamedSharding):
    return NamedShardingMetadata.from_jax_sharding(jax_sharding)
  elif isinstance(jax_sharding, jax.sharding.SingleDeviceSharding):
    return SingleDeviceShardingMetadata.from_jax_sharding(jax_sharding)
  else:
    logging.warning(
        'Conversion for %s has not been implemented.', type(jax_sharding)
    )

