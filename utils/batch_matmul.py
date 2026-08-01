
def batch_matmul(lhs: Array, rhs: Array,
                 precision: PrecisionLike = None) -> Array:
  """Batch matrix multiplication."""
  if _min(lhs.ndim, rhs.ndim) < 2:
    raise ValueError('Arguments to batch_matmul must be at least 2D, got {}, {}'
                     .format(lhs.ndim, rhs.ndim))
  if lhs.ndim != rhs.ndim:
    raise ValueError('Arguments to batch_matmul must have same ndim, got {}, {}'
                     .format(lhs.ndim, rhs.ndim))
  lhs_contract = (lhs.ndim - 1,)
  rhs_contract = (rhs.ndim - 2,)
  batch = tuple(range(lhs.ndim - 2))
  return dot_general(lhs, rhs, ((lhs_contract, rhs_contract), (batch, batch)),
                     precision=precision)

