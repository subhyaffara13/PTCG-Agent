
def are_all_shardings_default_mem_kind(shardings):
  for i in shardings:
    if isinstance(i, UnspecifiedValue):
      continue
    mem_kind = (core.mem_space_to_kind(i) if isinstance(i, core.MemorySpace)
                else i.memory_kind)
    if mem_kind is None:
      continue
    if mem_kind != 'device':
      return False
  return True

