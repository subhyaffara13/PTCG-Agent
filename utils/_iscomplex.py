
def _iscomplex(x) -> bool:
  return dtypes.issubdtype(_dtype(x), np.complexfloating)

