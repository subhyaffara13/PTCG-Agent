
def _np_convert_in_place(d):
  """Convert any jax devicearray leaves to numpy arrays in place."""
  if isinstance(d, dict):
    for k, v in d.items():
      if isinstance(v, jax.Array):
        d[k] = np.array(v)
      elif isinstance(v, dict):
        _np_convert_in_place(v)
  elif isinstance(d, jax.Array):
    return np.array(d)
  return d


def _np_convert_in_place(d):
  """Convert any jax devicearray leaves to numpy arrays in place."""
  if isinstance(d, dict):
    for k, v in d.items():
      if isinstance(v, jax.Array):
        d[k] = np.array(v)
      elif isinstance(v, dict):
        _np_convert_in_place(v)
  elif isinstance(d, jax.Array):
    return np.array(d)
  return d

