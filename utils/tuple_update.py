
def tuple_update(t: tuple[T, ...], idx: int, val: T) -> tuple[T, ...]:
  assert 0 <= idx < len(t), (idx, len(t))
  return t[:idx] + (val,) + t[idx+1:]

