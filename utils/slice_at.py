
def slice_at(t: tuple, index: int | None) -> tuple[tp.Any, tuple]:
  if index is None:
    return None, t
  return t[index], t[:index] + t[index + 1 :]

