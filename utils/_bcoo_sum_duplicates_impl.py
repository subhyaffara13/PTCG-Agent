
def _bcoo_sum_duplicates_impl(data, indices, *, spinfo, nse):
  props = _validate_bcoo(data, indices, spinfo.shape)
  indices_out, mapping, nse_batched = _unique_indices(
    indices, shape=spinfo.shape, return_inverse=True, return_true_size=True)
  if nse is None:
    nse = 1 if props.n_sparse == 0 else nse_batched.max()
  indices_out = _adjust_indices_nse(indices_out, nse=nse, shape=spinfo.shape)
  if props.n_sparse == 0:
    data = data.sum(props.n_batch, keepdims=True, dtype=data.dtype)
  data_out = jnp.zeros((*map(max, indices.shape[:props.n_batch], data.shape[:props.n_batch]),
                        nse, *data.shape[props.n_batch + 1:]), dtype=data.dtype)
  permute = lambda d_out, m, d: d_out.at[m].add(d, mode='drop')
  permute = nfold_vmap(permute, props.n_batch)
  data_out = permute(data_out, mapping, data)
  return data_out, indices_out

