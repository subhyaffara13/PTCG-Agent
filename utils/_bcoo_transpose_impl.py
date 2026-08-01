
def _bcoo_transpose_impl(data, indices, *, permutation: Sequence[int], spinfo: SparseInfo):
  batch_perm, sparse_perm, dense_perm = _validate_permutation(data, indices, permutation, spinfo.shape)
  n_batch = len(batch_perm)
  indices = indices[..., sparse_perm].transpose(*batch_perm, n_batch, n_batch + 1)
  data = data.transpose(*batch_perm, n_batch, *(d + n_batch + 1 for d in dense_perm))
  return data, indices

