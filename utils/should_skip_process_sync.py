from typing import Optional, Set

def should_skip_process_sync(processes: Optional[Set[int]] = None) -> bool:
  if processes and len(processes) == 1 and process_index() in processes:
    return True
  if jax.process_count() == 1:
    return True
  return False


def should_skip_process_sync(processes: Collection[int] | None = None) -> bool:
  if processes and len(processes) == 1 and process_index() in processes:
    return True
  if jax.process_count() == 1:
    return True
  if is_pathways_backend():
    return True
  return False

