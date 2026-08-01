
def _triu(m: Array, k:int = 0) -> Array:
  *_, N, M = m.shape
  mask = lax._tri(bool, (N, M), k - 1)
  return lax.select(lax.broadcast(mask, m.shape[:-2]), lax.full_like(m, 0), m)

