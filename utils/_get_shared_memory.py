
def _get_shared_memory() -> memory.GPUSharedMemory:
  assert _shared_memory is not None
  return _shared_memory


def _get_shared_memory() -> memory.SharedMemory:
  assert _shared_memory is not None
  return _shared_memory

