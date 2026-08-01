
def _humanize_worker_memory_usage(
    worker_memory_usage: dict[int, int],
) -> dict[str, str]:
  return {
      f'worker_{worker_id}': humanize.naturalsize(memory_usage, binary=True)
      for worker_id, memory_usage in worker_memory_usage.items()
  }

