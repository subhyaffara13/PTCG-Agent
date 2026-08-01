
def copy_vector_clock(x: VectorClock | None) -> VectorClock | None:
  if x is None:
    return None
  return x.copy()

