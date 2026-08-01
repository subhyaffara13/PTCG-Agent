
def insert_at(t: tuple, index: int | None, value: tp.Any) -> tuple:
  if index is None:
    return t
  xs = list(t)
  xs.insert(index, value)
  return tuple(xs)

