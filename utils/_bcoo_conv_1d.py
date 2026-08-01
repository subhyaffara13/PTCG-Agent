
def _bcoo_conv_1d(lhs: BCOO, rhs: BCOO, padding: Sequence[int]) -> BCOO:
  assert lhs.ndim == lhs.n_sparse == rhs.ndim == rhs.n_sparse == 1
  assert lhs.dtype == rhs.dtype
  padding = tuple(map(int, padding))
  assert len(padding) == 2

  new_data = (lhs.data[:, None] * rhs.data[None, :]).ravel()

  offset = padding[0] - rhs.indices
  new_indices = (lhs.indices[:, None] + offset[None, :]).ravel()

  mask = (new_indices < 0)
  new_indices = jnp.where(mask, 0, new_indices)
  new_data = jnp.where(mask, 0, new_data)
  dimsize = max(0, lhs.shape[0] + padding[0] + padding[1] - rhs.shape[0] + 1)

  new_data = lax.expand_dims(new_data, (0, 1))
  new_indices = lax.expand_dims(new_indices, (0, 1, 3))
  return BCOO((new_data, new_indices), shape=(1, 1, dimsize))

