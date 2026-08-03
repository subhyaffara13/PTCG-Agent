import math


def get_leaf_memory_per_device(arr: jax.Array) -> int:
  """Returns the memory usage of a sharded array per device (in bytes)."""
  shard_shape = arr.sharding.shard_shape(arr.shape)
  return math.prod(shard_shape) * arr.dtype.itemsize

