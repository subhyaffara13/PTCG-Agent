
def _bcoo_sort_indices_impl(data, indices, *, spinfo):
  props = _validate_bcoo(data, indices, spinfo.shape)
  if props.n_sparse == 0:
    return data, indices
  f = nfold_vmap(_bcoo_sort_indices_unbatched, props.n_batch, broadcasted=False)
  indices, perm = f(indices)
  permute = nfold_vmap(lambda d, p: d[p], props.n_batch)
  data = permute(data, perm)
  return data, indices

