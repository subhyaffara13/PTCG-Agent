
def _bcoo_to_bcsr(indices: Array, *, shape: Sequence[int],
                  index_dtype: DTypeLike) -> tuple[Array, Array]:
  """Given BCOO (indices), return BCSR (indices, indptr).

  Note: this assumes that ``indices`` are lexicographically sorted within each batch.
  """
  n_batch, n_sparse, _, _ = bcoo._validate_bcoo_indices(indices, shape)

  if n_sparse != 2:
    raise ValueError("Must have 2 sparse dimensions to be converted to BCSR.")

  n_rows = shape[n_batch]

  @partial(nfold_vmap, N=n_batch, broadcasted=False)
  def get_ptr(i):
    indptr = jnp.zeros(n_rows + 1, index_dtype)
    return indptr.at[1:].set(jnp.cumsum(
        jnp.bincount(i, length=n_rows).astype(index_dtype)))

  return indices[..., 1], get_ptr(indices[..., 0])

