
def _csr_transpose(data, indices, indptr):
  # Transpose of a square CSR matrix
  m = indptr.size - 1
  row = jnp.cumsum(jnp.zeros_like(indices).at[indptr].add(1)) - 1
  row_T, indices_T, data_T = jax.lax.sort((indices, row, data), num_keys=2)
  indptr_T = jnp.zeros_like(indptr).at[1:].set(
      jnp.cumsum(jnp.bincount(row_T, length=m)).astype(indptr.dtype))
  return data_T, indices_T, indptr_T

