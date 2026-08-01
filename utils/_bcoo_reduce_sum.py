
def _bcoo_reduce_sum(data: Array, indices: Array, *, spinfo: SparseInfo, axes: Sequence[int]) -> tuple[Array, Array, Shape]:
  shape = spinfo.shape
  assert all(0 <= a < len(shape) for a in axes)
  n_batch, n_sparse, _, nse = _validate_bcoo(data, indices, shape)
  axes = sorted(set(axes))

  # Sum over dense dimensions -> sum over data
  dense_axes = tuple(ax - n_sparse + 1 for ax in axes if ax >= n_batch + n_sparse)
  data = data.sum(dense_axes)
  if n_sparse:
    # zero-out data corresponding to invalid indices.
    fill_value = jnp.expand_dims(
      jnp.array(shape[n_batch: n_batch + n_sparse], dtype=indices.dtype),
      range(indices.ndim - 1))
    mask = jnp.all(indices < fill_value, -1)
    if data.ndim > mask.ndim:
      mask = lax.expand_dims(mask, tuple(range(mask.ndim, data.ndim)))
    data = jnp.where(mask, data, 0)

  # Sum over sparse dimensions -> drop index; sum is implicit
  sparse_idx = [i for i in range(n_sparse) if i + n_batch not in axes]
  if not sparse_idx:
    indices = jnp.zeros(_tuple_replace(indices.shape, n_batch + 1, 0), indices.dtype)
  else:
    indices = indices[..., np.array(sparse_idx)]

  # Sum over batch dimensions -> reshape into nse
  batch_axes = {ax for ax in axes if ax < n_batch}

  # First handle broadcasted batch dimensions
  for ax in batch_axes:
    if data.shape[ax] == 1:
      if indices.shape[ax] == 1:
        data = data * shape[ax]
      else:
        data = lax.broadcast_in_dim(data, _tuple_replace(data.shape, ax, shape[ax]), tuple(range(data.ndim)))
    else:
      if indices.shape[ax] == 1:
        data = data.sum(ax)
    assert data.shape[ax] == indices.shape[ax]

  new_batch_dims = tuple(sorted(set(range(n_batch)) - batch_axes))
  new_batch_shape = tuple(data.shape[i] for i in new_batch_dims)
  new_nse = nse * math.prod([data.shape[i] for i in batch_axes])

  data = lax.reshape(data,
                     (*new_batch_shape, new_nse, *data.shape[n_batch + 1:]),
                     (*new_batch_dims, *batch_axes, *range(n_batch, data.ndim)))
  indices = lax.reshape(indices,
                        (*new_batch_shape, new_nse, *indices.shape[n_batch + 1:]),
                        (*new_batch_dims, *batch_axes, *range(n_batch, indices.ndim)))

  out_shape = tuple(shape[i] for i in range(len(shape)) if i not in axes)
  return data, indices, out_shape

