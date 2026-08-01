
def _bcoo_fromdense_impl(mat, *, nse, n_batch, n_dense, index_dtype):
  mat = jnp.asarray(mat)
  n_sparse = mat.ndim - n_dense - n_batch
  mask = (mat != 0)
  if n_dense > 0:
    mask = mask.any([-(i + 1) for i in range(n_dense)])
  @partial(nfold_vmap, N=n_batch, broadcasted=False)
  def _nonzero(a):
    if a.ndim:
      return jnp.nonzero(a, size=nse, fill_value=a.shape[:n_sparse])
    return ()
  indices = _nonzero(mask)
  if not indices:
    indices = jnp.zeros(mask.shape[:n_batch] + (nse, 0), index_dtype)
  else:
    indices = jnp.moveaxis(jnp.array(indices, index_dtype), 0, n_batch + 1)
  data = _bcoo_extract(indices, mat)

  true_nse = mask.sum(list(range(n_batch, mask.ndim)))[..., None]
  true_nonzeros = lax.broadcasted_iota(true_nse.dtype, (1,) * n_batch + (nse,), n_batch) < true_nse
  true_nonzeros = true_nonzeros[(n_batch + 1) * (slice(None),) + n_dense * (None,)]
  data = jnp.where(true_nonzeros, data, 0)

  return data, indices

