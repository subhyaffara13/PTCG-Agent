
def _bcoo_sort_indices_unbatched(indices):
  # sort indices without summing duplicates
  nse, N = indices.shape
  idx_cols = (indices[:, i] for i in range(N))
  *indices, perm = lax.sort((*idx_cols, lax.iota(indices.dtype, nse)), num_keys=N)
  return jnp.column_stack(indices), perm

