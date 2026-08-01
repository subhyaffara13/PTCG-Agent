
def _lu_blocked(a, block_size=128):
  """Blocked LU decomposition, as an unrolled loop."""
  m, n = a.shape
  r = min(m, n)
  pivot = lax.full((r,), 0, dtype=np.int32)
  perm = lax.iota('int32', m)
  for k in range(0, r, block_size):
    b = min(r - k, block_size)
    block_pivot, block_perm, lu_block = _lu_unblocked(a[k:, k:k+b])

    pivot = pivot.at[k:k+b].set(block_pivot + k)
    perm = perm.at[k:].set(perm[block_perm + k])
    a = a.at[k:, :].set(a[block_perm + k, :])
    a = a.at[k:, k:k+b].set(lu_block)

    if k + b < n:
      a = a.at[k:k+b, k+b:].set(
        triangular_solve(a[k:k+b, k:k+b], a[k:k+b, k+b:], left_side=True,
                         lower=True, unit_diagonal=True))
      a = a.at[k+b:, k+b:].add(-lax.dot(a[k+b:, k:k+b], a[k:k+b, k+b:],
                                        precision=lax.Precision.HIGHEST))
  return a, pivot, perm

