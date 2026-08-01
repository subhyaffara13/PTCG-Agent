
def _transpose_sparse(spenv, *spvalues, permutation):
  permutation = tuple(permutation)
  args = spvalues_to_arrays(spenv, spvalues)
  shape = args[0].shape
  mat_transposed = sparse.bcoo_transpose(args[0], permutation=permutation)
  out_shape = tuple(shape[i] for i in permutation)

  n_batch = args[0].indices.ndim - 2
  n_sparse = args[0].indices.shape[-1]
  batch_dims_unchanged = (permutation[:n_batch] == tuple(range(n_batch)))
  dense_dims_unchanged = (permutation[n_batch + n_sparse:] == tuple(range(n_batch + n_sparse, len(shape))))
  sparse_dims_unchanged = (permutation[n_batch:n_batch + n_sparse] == tuple(range(n_batch, n_batch + n_sparse)))

  # Data is unchanged if batch & dense dims are not permuted
  kwds = {}
  if batch_dims_unchanged and dense_dims_unchanged:
    kwds['data_ref'] = spvalues[0].data_ref
  else:
    kwds['data'] = mat_transposed.data

  # Indices unchanged if batch & sparse dims are not permuted
  if batch_dims_unchanged and sparse_dims_unchanged:
    kwds['indices_ref'] = spvalues[0].indices_ref
  else:
    kwds['indices'] = mat_transposed.indices

  kwds['indices_sorted'] = mat_transposed.indices_sorted
  kwds['unique_indices'] = mat_transposed.unique_indices
  spvalue = spenv.sparse(out_shape, **kwds)
  return (spvalue,)

