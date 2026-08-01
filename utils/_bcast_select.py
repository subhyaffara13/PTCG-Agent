
def _bcast_select(pred, on_true, on_false):
  if np.ndim(pred) != np.ndim(on_true):
    idx = list(range(np.ndim(pred)))
    pred = lax.broadcast_in_dim(pred, np.shape(on_true), idx)
  return lax.select(pred, on_true, on_false)

