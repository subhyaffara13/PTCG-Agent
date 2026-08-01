
def _update_clocks_for_global_barrier():
  """Synchronizes all vector clocks."""
  shared_memory = _get_shared_memory()
  shared_memory.update_clocks(0, shared_memory.num_cores)

