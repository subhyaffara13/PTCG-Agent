
def _bcsr_extract_impl(indices, indptr, mat):
  mat = jnp.asarray(mat)
  bcoo_indices = _bcsr_to_bcoo(indices, indptr, shape=mat.shape)
  return bcoo._bcoo_extract(bcoo_indices, mat)

