
def _bcoo_multiply_sparse_unbatched(lhs_data, lhs_indices, rhs_data, rhs_indices, *, lhs_shape, rhs_shape):
  lhs = _validate_bcoo(lhs_data, lhs_indices, lhs_shape)
  rhs = _validate_bcoo(rhs_data, rhs_indices, rhs_shape)
  assert (lhs.n_batch == 0) or (rhs.n_batch == 0)  # Ensured at call site above

  # TODO(jakevdp): this can be made more efficient by utilizing batch structure.
  if lhs.n_batch:
    lhs_data, lhs_indices = bcoo_update_layout(BCOO((lhs_data, lhs_indices), shape=lhs_shape), n_batch=0)._bufs
    lhs = _validate_bcoo(lhs_data, lhs_indices, lhs_shape)
  elif rhs.n_batch:
    rhs_data, rhs_indices = bcoo_update_layout(BCOO((rhs_data, rhs_indices), shape=rhs_shape), n_batch=0)._bufs
    rhs = _validate_bcoo(rhs_data, rhs_indices, rhs_shape)
  dims = jnp.array([i for i, (s1, s2) in enumerate(safe_zip(lhs_shape[:lhs.n_sparse], rhs_shape[:rhs.n_sparse]))
                    if s1 != 1 and s2 != 1], dtype=int)

  # TODO(jakevdp): this nse can be tightened to min(lhs.nse, rhs.nse) if there
  # is no broadcasting and indices are unique.
  nse = lhs.nse * rhs.nse

  # TODO(jakevdp): this is pretty inefficient. Can we do this membership check
  # without constructing the full (lhs.nse, rhs.nse) masking matrix?
  mask = jnp.all(lhs_indices[:, None, dims] == rhs_indices[None, :, dims], -1)
  i_lhs, i_rhs = jnp.nonzero(mask, size=nse, fill_value=(lhs.nse, rhs.nse))
  data = (lhs_data.at[i_lhs].get(mode='fill', fill_value=0) *
          rhs_data.at[i_rhs].get(mode='fill', fill_value=0))
  indices = jnp.maximum(
      lhs_indices.at[i_lhs].get(mode='fill', fill_value=max(lhs_shape, default=0)),
      rhs_indices.at[i_rhs].get(mode='fill', fill_value=max(rhs_shape, default=0)))
  return data, indices

