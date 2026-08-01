
def mem_space_to_kind(mem_space: MemorySpace) -> str:
  if mem_space == MemorySpace.Device:
    return 'device'
  elif mem_space == MemorySpace.Host:
    return 'pinned_host'
  else:
    assert False, "unreachable"

