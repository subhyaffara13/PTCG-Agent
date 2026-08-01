
def _bcoo_sum_duplicates_jvp(primals, tangents, *, spinfo, nse):
  data, indices = primals
  props = _validate_bcoo(data, indices, spinfo.shape)

  data_dot, _ = tangents
  indices_out, mapping, nse_batched = _unique_indices(
    indices, shape=spinfo.shape, return_inverse=True, return_true_size=True)
  if nse is None:
    nse = jnp.sum(nse_batched)
  try:
    nse = core.concrete_or_error(operator.index, nse, "nse argument of bcoo_sum_duplicates.")
  except core.ConcretizationTypeError:
    raise ValueError("bcoo_sum_duplicates: nse must be specified when using the function within "
                     "jit, vmap, and other transformations requiring abstract evaluation.")
  indices_out = _adjust_indices_nse(indices_out, nse=nse, shape=spinfo.shape)
  if props.n_sparse == 0:
    data = data.sum(props.n_batch, keepdims=True, dtype=data.dtype)
    data_dot = data_dot.sum(props.n_batch, keepdims=True, dtype=data_dot.dtype)
  data_out = jnp.zeros((*map(max, indices.shape[:props.n_batch], data.shape[:props.n_batch]),
                        nse, *data.shape[props.n_batch + 1:]), dtype=data.dtype)
  data_dot_out = data_out
  # This check is because scatter-add on zero-sized arrays has poorly defined
  # semantics; see https://github.com/jax-ml/jax/issues/13656.
  if data_out.size:
    permute = lambda x, i, y: x.at[i].add(y, mode='drop')
  else:
    permute = lambda x, i, y: x
  permute = nfold_vmap(permute, props.n_batch)
  data_out = permute(data_out, mapping, data)
  indices_dot_out = ad.p2tz(indices_out)
  data_dot_out = ad.p2tz(data_out) if type(data_dot) is ad.Zero else permute(data_dot_out, mapping, data_dot)
  return (data_out, indices_out), (data_dot_out, indices_dot_out)

