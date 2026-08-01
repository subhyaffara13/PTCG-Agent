
def _bcoo_todense_impl(data, indices, *, spinfo):
  shape = spinfo.shape
  n_batch, n_sparse, _, _ = _validate_bcoo(data, indices, shape)

  ind_slices = tuple(np.zeros(s, int) if i_s == 1 else np.arange(s)
                     for s, i_s in zip(shape[:n_batch], indices.shape[:n_batch]))
  grid = tuple(np.meshgrid(*ind_slices, indexing='ij', sparse=True))
  sparse_ind = tuple(indices[grid + (slice(None), i)] for i in range(n_sparse))

  batch_slices = tuple(np.arange(s) for s in shape[:n_batch])
  grid = np.meshgrid(*batch_slices, np.arange(1), indexing='ij', sparse=True)
  batch_ind = tuple(grid)[:-1]

  if not sparse_ind:
    data = data.sum(n_batch, keepdims=bool(batch_ind), dtype=data.dtype)
  return jnp.zeros(shape, data.dtype).at[batch_ind + sparse_ind].add(data)

