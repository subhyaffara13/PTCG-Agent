
def bcoo_eliminate_zeros(mat: BCOO, nse: int | None = None) -> BCOO:
  data, indices, shape = mat.data, mat.indices, mat.shape
  props = _validate_bcoo(data, indices, shape)
  mask = (data == 0).all(tuple(range(props.n_batch + 1, data.ndim)))
  dims_to_contract = tuple(i for i, s in enumerate(indices.shape[:props.n_batch]) if s == 1)
  mask = mask.all(dims_to_contract, keepdims=True)
  fill_value = jnp.array(shape[props.n_batch:props.n_batch + props.n_sparse], dtype=indices.dtype)
  f = lambda i, m: jnp.where(m[:, None], fill_value[None, :], i)
  indices = nfold_vmap(f, props.n_batch)(indices, mask)
  return bcoo_sum_duplicates(BCOO((data, indices), shape=shape), nse=nse)

