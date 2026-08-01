
def _empty_svd(a, *, full_matrices, compute_uv):
  batch_shape = a.shape[:-2]
  m, n = a.shape[-2:]
  s = lax.full(batch_shape + (0,), 0, dtype=lax._complex_basetype(a.dtype))
  if not compute_uv:
    return (s,)
  if full_matrices:
    size = max(m, n)
    u = lax.broadcast_in_dim(lax._eye(a.dtype, (size, size)),
                             (*batch_shape, size, size),
                             (len(batch_shape), len(batch_shape) + 1))
  else:
    u = lax.full(batch_shape + (m, n), 0, dtype=a.dtype)
  v = lax.full(batch_shape + (0, 0), 0, dtype=a.dtype)
  if m < n:
    u, v = v, u
  return s, u, v

