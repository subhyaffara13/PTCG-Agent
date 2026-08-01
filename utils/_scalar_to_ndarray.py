
def _scalar_to_ndarray(x, shape=None):
  return np.broadcast_to(x, shape or DEFAULT_NDARRAY_PARAMS_SHAPE)

