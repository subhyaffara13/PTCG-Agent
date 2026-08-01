
def _tril(m: Array, k:int = 0) -> Array:
  *_, N, M = m.shape
  mask = lax._tri(bool, (N, M), k)
  return lax.select(lax.broadcast(mask, m.shape[:-2]), m, lax.full_like(m, 0))

