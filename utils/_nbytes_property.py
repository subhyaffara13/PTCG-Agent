
def _nbytes_property(self: Array) -> int:
  """Total bytes consumed by the elements of the array."""
  return np.size(self) * self.dtype.itemsize

