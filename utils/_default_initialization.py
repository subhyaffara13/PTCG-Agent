
def _default_initialization(x):
  assert hasattr(x, 'shape')
  assert hasattr(x, 'dtype')
  dtype = np.dtype(x)
  if np.issubdtype(dtype, np.integer):
    value = np.iinfo(dtype).min
  else:
    value = math.nan
  return lax.full(x.shape, value, dtype)

