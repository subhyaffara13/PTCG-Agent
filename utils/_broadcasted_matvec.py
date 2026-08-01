
def _broadcasted_matvec(a: Array, b: Array) -> Array:
  # This is a broadcasted dot_general with signature (...,n,m),(...,m)->(...,n)
  assert a.ndim >= 2
  assert b.ndim >= 1
  batch_shape = lax.broadcast_shapes(a.shape[:-2], b.shape[:-1])
  n_batch = len(batch_shape)
  a = _broadcast_to(a, (*batch_shape, *a.shape[-2:]))
  b = _broadcast_to(b, (*batch_shape, b.shape[-1]))

  dimension_numbers = (([a.ndim - 1], [b.ndim - 1]), (list(range(n_batch)), list(range(n_batch))))
  return lax.dot_general(a, b, dimension_numbers=dimension_numbers, precision=lax.Precision.HIGHEST)

