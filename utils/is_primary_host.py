from typing import Optional

def is_primary_host(primary_host: Optional[int]):
  if primary_host is None or primary_host == process_index():
    return True
  return False


def is_primary_host(primary_host: int | None):
  if primary_host is None or primary_host == process_index():
    return True
  return False

