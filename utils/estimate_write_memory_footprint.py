
def estimate_write_memory_footprint(arr: np.ndarray) -> int:
  return arr.size * arr.dtype.itemsize

