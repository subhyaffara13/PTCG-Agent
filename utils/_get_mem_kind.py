
def _get_mem_kind(s: JSharding | None) -> str | None:
  if s is None:
    return None
  assert isinstance(s, JSharding)
  return s.memory_kind

