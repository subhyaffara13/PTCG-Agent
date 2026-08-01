
def broadcast_to_rank(x: ArrayLike, rank: int) -> Array:
  """Adds leading dimensions of ``1`` to give ``x`` rank ``rank``."""
  ndim = np.ndim(x)
  if ndim == rank:
    return asarray(x)
  return broadcast(x, (1,) * (rank - ndim))

