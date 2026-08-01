
def _bcoo_extract_impl(indices, arr, *, assume_unique):
  arr = jnp.asarray(arr)
  props = _validate_bcoo_indices(indices, arr.shape)
  original_props = props
  if not assume_unique:
    indices, sort_ind = _unique_indices(indices, shape=arr.shape, return_index=True)
    props = _validate_bcoo_indices(indices, arr.shape)
  else:
    sort_ind = ...

  ind_slices = tuple(np.zeros(s, int) if i_s == 1 else np.arange(s)
                     for s, i_s in zip(arr.shape[:props.n_batch], indices.shape[:props.n_batch]))
  grid = tuple(np.meshgrid(*ind_slices, indexing='ij', sparse=True))
  sparse_ind = tuple(indices[grid + (slice(None), i)] for i in range(props.n_sparse))

  batch_slices = tuple(np.arange(s) for s in arr.shape[:props.n_batch])
  grid = np.meshgrid(*batch_slices, np.arange(1), indexing='ij', sparse=True)
  batch_ind = tuple(grid)[:-1]

  if not sparse_ind + batch_ind:
    result = arr[None]
  else:
    result = arr.at[batch_ind + sparse_ind].get(mode='fill', fill_value=0)
  if props.n_sparse == 0 and props.nse != 1:
    if assume_unique:
      result = lax.broadcast_in_dim(
        result, _tuple_replace(result.shape, props.n_batch, props.nse), range(result.ndim))
    else:
      out_shape = _tuple_replace(result.shape, props.n_batch, original_props.nse)
      ind = props.n_batch * (slice(None),) + (slice(1),)
      result = jnp.zeros_like(result, shape=out_shape).at[ind].set(result)
  if not assume_unique:
    unbatched_out_shape = (original_props.nse, *result.shape[props.n_batch + 1:])
    def f(r, i):
      return jnp.zeros_like(r, shape=unbatched_out_shape).at[i].add(r)
    for _ in range(props.n_batch):
      f = vmap(f)
    result = f(result, sort_ind)
  return result

