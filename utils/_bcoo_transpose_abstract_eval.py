
def _bcoo_transpose_abstract_eval(data, indices, *, permutation: Sequence[int], spinfo: SparseInfo):
  batch_perm, _, dense_perm = _validate_permutation(data, indices, permutation, spinfo.shape)
  n_batch = len(batch_perm)
  indices_shape = np.array(indices.shape)[[*batch_perm, n_batch, n_batch + 1]]
  data_shape = np.array(data.shape)[[*batch_perm, n_batch, *(d + n_batch + 1 for d in dense_perm)]]
  return core.ShapedArray(data_shape, data.dtype), core.ShapedArray(indices_shape, indices.dtype)

