
def mem_kind_to_space(mem_kind: str | None) -> MemorySpace:
  if mem_kind == 'pinned_host':
    return MemorySpace.Host
  return MemorySpace.Device

