
def _lu_python(x):
  """Default LU decomposition in Python, where no better version exists."""
  batch_dims = x.shape[:-2]
  fn = _lu_blocked
  for _ in range(len(batch_dims)):
    fn = api.vmap(fn)

  return fn(x)

