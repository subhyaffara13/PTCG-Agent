
def _get_updates_batching_dims(indices_batching_dims, update_window_dims,
                               index_vector_dim, updates_shape):
  scatter_dim_in_updates: list[int | None] = list(range(index_vector_dim))
  for i in update_window_dims:
    scatter_dim_in_updates.insert(i, None)
  assert len(scatter_dim_in_updates) == len(updates_shape)
  return tuple(scatter_dim_in_updates.index(i) for i in indices_batching_dims)

