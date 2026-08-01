
def _normalize_matvec(f):
  """Normalize an argument for computing matrix-vector products."""
  if callable(f):
    return f
  elif isinstance(f, (np.ndarray, Array)):
    if f.ndim != 2 or f.shape[0] != f.shape[1]:
      raise ValueError(
          f'linear operator must be a square matrix, but has shape: {f.shape}')
    return partial(_dot, f)
  elif hasattr(f, '__matmul__'):
    if hasattr(f, 'shape') and len(f.shape) != 2 or f.shape[0] != f.shape[1]:
      raise ValueError(
          f'linear operator must be a square matrix, but has shape: {f.shape}')
    return partial(operator.matmul, f)
  else:
    raise TypeError(
        f'linear operator must be either a function or ndarray: {f}')

