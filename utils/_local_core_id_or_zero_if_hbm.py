
def _local_core_id_or_zero_if_hbm(local_core_id: int, memory_space: str) -> int:
  if memory_space in ['any', 'hbm']:
    return 0
  return local_core_id

