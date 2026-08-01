
def _get_leaf_pspec(x: Any) -> jax.sharding.PartitionSpec | None:
  if hasattr(x, 'get_partition_spec'):
    return x.get_partition_spec()
  # Unboxed arrays, which should be replicated across all devices
  elif hasattr(x, 'shape'):
    return jax.sharding.PartitionSpec()
  else:
    return None

