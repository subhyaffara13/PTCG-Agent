
def _bcast_select_n(pred, *cases):
  if np.ndim(pred) != np.ndim(cases[0]):
    idx = list(range(np.ndim(pred)))
    pred = lax.broadcast_in_dim(pred, np.shape(cases[0]), idx)
  return lax.select_n(pred, *cases)

