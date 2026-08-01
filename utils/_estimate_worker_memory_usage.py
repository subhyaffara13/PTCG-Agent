
def _estimate_worker_memory_usage(
    arr: jax.Array,
    *,
    replica_id: int | None,
    device_to_worker_ids_map: dict[int, int],
) -> dict[int, int]:
  """Estimates memory used by the array on each worker after transfer.

  Args:
    arr: The array to estimate memory usage for.
    replica_id: The replica id to use for estimation. If None, all replicas are
      used.
    device_to_worker_ids_map: A mapping from device ID to worker ID.

  Returns:
    A mapping from worker ID to estimated memory usage.
  """
  worker_memory_usage = collections.defaultdict(int)
  shard_memory_size = (
      np.prod(arr.sharding.shard_shape(arr.shape)) * arr.dtype.itemsize
  )
  for shard in arr.global_shards:
    if replica_id is not None and shard.replica_id != replica_id:
      continue
    worker_id = device_to_worker_ids_map[shard.device.id]
    worker_memory_usage[worker_id] += shard_memory_size
  return worker_memory_usage

