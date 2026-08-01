
def _qr_shape_rule(shape, *, pivoting, full_matrices, **_):
  m, n = shape
  k = m if full_matrices else core.min_dim(m, n)
  return ((m, k), (k, n), (n,)) if pivoting else ((m, k), (k, n))

