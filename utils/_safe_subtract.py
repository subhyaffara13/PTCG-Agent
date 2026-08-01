
def _safe_subtract(x, y, *, dtype):
  """Subtraction that with `inf - inf == 0` semantics."""
  with np.errstate(invalid='ignore'):
    return np.where(np.equal(x, y), np.array(0, dtype),
                    np.subtract(x, y, dtype=dtype))

