
def _preprocess_none(t) -> np.ndarray:
  if t is None:
    return np.array(0.0, dtype=np.float32)
  else:
    return np.asarray(t)

