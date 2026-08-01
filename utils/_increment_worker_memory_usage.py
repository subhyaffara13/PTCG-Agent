
def _increment_worker_memory_usage(
    arr: jax.Array,
    current_worker_memory_usage: dict[int, int],
    *,
    replica_id: int | None,
    device_to_worker_ids_map: dict[int, int],
) -> dict[int, int]:
  """Increments memory used by the array on each worker after transfer."""
  estimate = _estimate_worker_memory_usage(
      arr,
      replica_id=replica_id,
      device_to_worker_ids_map=device_to_worker_ids_map,
  )
  return {
      worker_id: current_worker_memory_usage[worker_id] + estimate[worker_id]
      for worker_id in current_worker_memory_usage
  }

