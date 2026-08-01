
def _identity_getter(op):
  return lambda dtype: np.asarray(op.identity, dtype=dtype)

