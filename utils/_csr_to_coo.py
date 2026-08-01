
def _csr_to_coo(indices: Array, indptr: Array) -> tuple[Array, Array]:
  """Given CSR (indices, indptr) return COO (row, col)"""
  return jnp.cumsum(jnp.zeros_like(indices).at[indptr].add(1)) - 1, indices

