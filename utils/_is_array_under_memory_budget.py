
def _is_array_under_memory_budget(
    worker_memory_budget: int,
    incremented_worker_memory_usage: dict[int, int],
) -> bool:
  for _, worker_memory_usage in incremented_worker_memory_usage.items():
    if worker_memory_usage >= worker_memory_budget:
      return False
  return True

