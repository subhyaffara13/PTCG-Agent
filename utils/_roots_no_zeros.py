
def _roots_no_zeros(p: Array) -> Array:
  # build companion matrix and find its eigenvalues (the roots)
  if p.size < 2:
    return array([], dtype=dtypes.to_complex_dtype(p.dtype))
  A = diag(ones((p.size - 2,), p.dtype), -1)
  A = A.at[0, :].set(-p[1:] / p[0])
  return linalg.eigvals(A)

