
def get_expected_chunk_shape(
    arr: jax.Array,
    *,
    use_replica_parallel: bool = True,
    max_replicas_for_replica_parallel: Optional[bool] = None,
    pathways_support_replica_parallel: bool = False,
) -> tuple[int, ...]:
  """Expected chunk shape for an array, accounting for replica-parallel."""
  if not use_replica_parallel:
    return arr.sharding.shard_shape(arr.shape)
  _, local_shape, _ = (
      replica_slices.calculate_replica_parallel_axis_and_local_shape(
          arr, max_replicas_for_replica_parallel
      )
  )
  if local_shape is None:
    local_shape = arr.sharding.shard_shape(arr.shape)
  return local_shape

