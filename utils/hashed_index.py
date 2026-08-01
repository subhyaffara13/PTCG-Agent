
def hashed_index(x) -> int:
  assert all(v.step is None for v in x if isinstance(v, slice))
  return hash(tuple((v.start, v.stop) if isinstance(v, slice) else v for v in x))

