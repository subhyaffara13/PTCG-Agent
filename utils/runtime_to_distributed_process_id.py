
def runtime_to_distributed_process_id(pid: int) -> int:
  """Converts a distributed process index to a runtime process index."""
  if not is_runtime_to_distributed_ids_initialized():
    raise ValueError('Please call initialize_runtime_to_distributed_ids().')
  return _RUNTIME_TO_DISTRIBUTED_ID[pid]

