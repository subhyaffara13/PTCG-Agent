
def _qr_lowering(a, *, pivoting, full_matrices, use_magma):
  *batch_dims, m, n = a.shape
  if m == 0 or n == 0:
    k = m if full_matrices else core.min_dim(m, n)
    q = lax.broadcast_in_dim(lax._eye(a.dtype, (m, k)),
                             (*batch_dims, m, k),
                             (len(batch_dims), len(batch_dims) + 1))
    r = lax.full((*batch_dims, k, n), 0, dtype=a.dtype)
    if pivoting:
      p = lax.full((*batch_dims, n), 0, dtype=np.dtype(np.int32))
      return q, r, p
    return q, r

  p = None
  if pivoting:
    jpvt = lax.full((*batch_dims, n), 0, dtype=np.dtype(np.int32))
    r, p, taus = geqp3(a, jpvt, use_magma=use_magma)
    p -= 1  # Convert geqp3's 1-based indices to 0-based indices by subtracting 1.
  else:
    r, taus = geqrf(a)
    p = None

  if m < n:
    q = householder_product(r[..., :m, :m], taus)
  elif full_matrices:
    pads = [(0, 0, 0)] * (len(batch_dims) + 1) + [(0, m - n, 0)]
    q = lax.pad(r, lax._zero(r), pads)
    q = householder_product(q, taus)
  else:
    q = householder_product(r, taus)
    r = r[..., :n, :n]
  r = _triu(r)
  if pivoting:
    assert p is not None
    return q, r, p
  return q, r

