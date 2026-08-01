
def _chunk_array_leaves_in_place(d):
  """Convert oversized array leaves to safe chunked form in place."""
  if isinstance(d, dict):
    for k, v in d.items():
      if isinstance(v, np.ndarray):
        if v.size * v.dtype.itemsize > MAX_CHUNK_SIZE:
          d[k] = _chunk(v)
      elif isinstance(v, dict):
        _chunk_array_leaves_in_place(v)
  elif isinstance(d, np.ndarray):
    if d.size * d.dtype.itemsize > MAX_CHUNK_SIZE:
      return _chunk(d)
  return d


def _chunk_array_leaves_in_place(d):
  """Convert oversized array leaves to safe chunked form in place."""
  if isinstance(d, dict):
    for k, v in d.items():
      if isinstance(v, np.ndarray):
        if v.size * v.dtype.itemsize > MAX_CHUNK_SIZE:
          d[k] = _chunk(v)
      elif isinstance(v, dict):
        _chunk_array_leaves_in_place(v)
  elif isinstance(d, np.ndarray):
    if d.size * d.dtype.itemsize > MAX_CHUNK_SIZE:
      return _chunk(d)
  return d

