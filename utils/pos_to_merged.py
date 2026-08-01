
def pos_to_merged(pos: np.ndarray, size: int) -> int:
  """Converts a [x, y] position into a single integer."""
  assert (pos >= 0).all(), pos
  assert (pos < size).all(), pos
  return pos[0] + pos[1] * size


def pos_to_merged(pos: np.ndarray, size: int) -> int:
  """Converts a [x, y] position into a single integer."""
  assert (pos >= 0).all(), pos
  assert (pos < size).all(), pos
  return pos[0] + pos[1] * size

