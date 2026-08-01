
def normalized_by_sum(v: list, axis: int = 0) -> np.ndarray:
  """Divides each element of `v` along `axis` by the sum of `v` along `axis`."""
  v = np.asarray(v)
  s = v.sum(axis=axis, keepdims=True)
  return np.where(s == 0, 1.0 / v.shape[axis], v / np.where(s == 0, 1.0, s))

