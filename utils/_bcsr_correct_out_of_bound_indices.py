
def _bcsr_correct_out_of_bound_indices(data, indices, indptr, rhs, *, shape):
  props = _validate_bcsr(data, indices, indptr, shape)
  if props.n_batch:
    f = partial(_bcsr_correct_out_of_bound_indices, rhs=rhs, shape=shape[props.n_batch:])
    return nfold_vmap(f, props.n_batch)(data, indices, indptr)
  extent = indptr[-1]
  i_data = lax.broadcasted_iota(indptr.dtype, data.shape, 0)
  data = jnp.where(i_data < extent, data, 0)
  i_indices = lax.broadcasted_iota(indptr.dtype, indices.shape, 0)
  indices = jnp.where(i_indices < extent, indices, 0)
  return [data, indices]

