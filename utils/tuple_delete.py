
def tuple_delete(t: tuple[T, ...], idx: int) -> tuple[T, ...]:
  assert 0 <= idx < len(t), (idx, len(t))
  return t[:idx] + t[idx + 1:]


def tuple_delete(tup, idx):
  idx_ = set(idx)
  return tuple(tup[i] for i in range(len(tup)) if i not in idx_)

