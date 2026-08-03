from typing import Optional

def calculate_replica_parallel_axis_and_local_shape(
    arr: jax.Array, max_replicas_for_replica_parallel: Optional[int]
) -> OptionalAxisAndShapeAndReplicaCount:
  """Calculates a local shape for replica-parallel serialization."""
  shard0 = arr.addressable_shards[0]
  replica_count = _sharding_num_replicas(arr.sharding, arr.shape)
  if max_replicas_for_replica_parallel is not None:
    replica_count = min(replica_count, max_replicas_for_replica_parallel)
  if shard0.data.size == 0 or replica_count <= 1:
    return None, None, None
  try:
    axis = next(
        axis_index
        for axis_index, axis_size in enumerate(shard0.data.shape)
        if axis_size % replica_count == 0
    )
  except StopIteration:
    return None, None, None
  local_shape = tuple(
      axis_size // (replica_count if axis_index == axis else 1)
      for axis_index, axis_size in enumerate(shard0.data.shape)
  )
  return axis, local_shape, replica_count

