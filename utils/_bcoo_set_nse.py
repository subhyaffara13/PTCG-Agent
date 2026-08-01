
def _bcoo_set_nse(mat: BCOO, nse: int) -> BCOO:
  """Return a copy of `mat` with the specified nse.
  Note that if nse < mat.nse, this will potentially discard data.
  """
  nse = operator.index(nse)
  assert nse >= 0
  if mat.nse == nse:
    return mat
  if nse <= mat.nse:
    data = mat.data[(*(slice(None) for i in range(mat.n_batch)), slice(nse))]
    indices = mat.indices[..., :nse, :]
  else:
    data = jnp.zeros_like(mat.data, shape=(*mat.data.shape[:mat.n_batch], nse, *mat.data.shape[mat.n_batch + 1:]))
    data = data.at[(*(slice(None) for i in range(mat.n_batch)), slice(mat.nse))].set(mat.data)
    indices = jnp.zeros_like(mat.indices, shape=(*mat.indices.shape[:-2], nse, mat.indices.shape[-1]))
    indices = indices.at[..., :mat.nse, :].set(mat.indices)
    indices = indices.at[..., mat.nse:, :].set(jnp.array(mat.shape[mat.n_batch:mat.n_batch + mat.n_sparse],
                                                         dtype=indices.dtype))
  return BCOO((data, indices), shape=mat.shape,
              indices_sorted=mat.indices_sorted,
              unique_indices=mat.unique_indices)

