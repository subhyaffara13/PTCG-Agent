
def _bcsr_to_bcoo(indices: jax.Array, indptr: jax.Array, *,
                  shape: Sequence[int]) -> jax.Array:
  """Given BCSR (indices, indptr), return BCOO (indices)."""
  n_batch, _, _ = _validate_bcsr_indices(indices, indptr, shape)
  csr_to_coo = nfold_vmap(_csr_to_coo, n_batch)
  return jnp.stack(csr_to_coo(indices, indptr), axis=indices.ndim)

