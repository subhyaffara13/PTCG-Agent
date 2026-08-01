
def _bcoo_sort_indices_jvp(primals, tangents, *, spinfo):
  data, indices = primals

  props = _validate_bcoo(data, indices, spinfo.shape)
  if props.n_sparse == 0:
    return primals, tangents

  data_dot, _ = tangents
  f = nfold_vmap(_bcoo_sort_indices_unbatched, props.n_batch)
  indices_out, perm = f(indices)
  permute = nfold_vmap(lambda d, p: d[p], props.n_batch)
  data_out = permute(data, perm)

  indices_dot_out = ad.p2tz(indices)
  data_dot_out = ad.p2tz(data_out) if type(data_dot) is ad.Zero else permute(data_dot, perm)
  return (data_out, indices_out), (data_dot_out, indices_dot_out)

