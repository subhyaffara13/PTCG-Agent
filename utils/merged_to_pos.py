
def merged_to_pos(merged_pos: int, size: int) -> np.ndarray:
  """Inverse of pos_to_merged()."""
  assert 0 <= merged_pos < size * size
  return np.array([merged_pos % size, merged_pos // size])


def merged_to_pos(merged_pos: int, size: int) -> np.ndarray:
  """Inverse of pos_to_merged()."""
  assert 0 <= merged_pos < size * size
  return np.array([merged_pos % size, merged_pos // size])

