
def _bcoo_spdot_general_unbatched(lhs_data, lhs_indices, rhs_data, rhs_indices, *, lhs_spinfo, rhs_spinfo, lhs_contracting, rhs_contracting, out_nse):
  lhs_shape = lhs_spinfo.shape
  rhs_shape = rhs_spinfo.shape

  lhs = _validate_bcoo(lhs_data, lhs_indices, lhs_shape)
  rhs = _validate_bcoo(rhs_data, rhs_indices, rhs_shape)

  assert lhs.n_batch == rhs.n_batch == 0
  assert lhs.n_dense == rhs.n_dense == 0
  assert [lhs_shape[d] for d in lhs_contracting] == [rhs_shape[d] for d in rhs_contracting]
  assert max(lhs_contracting, default=-1) < lhs.n_sparse
  assert max(rhs_contracting, default=-1) < rhs.n_sparse

  out_shape = (
    *(s for i, s in enumerate(lhs_shape) if i not in lhs_contracting),
    *(s for i, s in enumerate(rhs_shape) if i not in rhs_contracting))

  lhs_i = lhs_indices[:, jnp.array(lhs_contracting, dtype=int)]
  rhs_i = rhs_indices[:, jnp.array(rhs_contracting, dtype=int)]
  lhs_j = lhs_indices[:, jnp.array(remaining(range(lhs.n_sparse), lhs_contracting), dtype=int)]
  rhs_j = rhs_indices[:, jnp.array(remaining(range(rhs.n_sparse), rhs_contracting), dtype=int)]

  # TODO(jakevdp): can we do this more efficiently than using an outer product? Note that
  #   jnp.isin() currently doesn't help much, because it also does all() over an outer
  #   comparison.
  overlap = (lhs_i[:, None] == rhs_i[None, :]).all(-1)
  lhs_fill_value = jnp.expand_dims(
    jnp.array([lhs_shape[d] for d in lhs_contracting], dtype=lhs_i.dtype),
    range(lhs_i.ndim - 1))
  rhs_fill_value = jnp.expand_dims(
    jnp.array([rhs_shape[d] for d in rhs_contracting], dtype=rhs_i.dtype),
    range(rhs_i.ndim - 1))
  lhs_valid = (lhs_i < lhs_fill_value).all(-1)
  rhs_valid = (rhs_i < rhs_fill_value).all(-1)
  out_data = jnp.where(overlap & lhs_valid[:, None] & rhs_valid[None, :],
                       lhs_data[:, None] * rhs_data[None, :], 0).ravel()

  out_indices = jnp.zeros([lhs.nse, rhs.nse, lhs_j.shape[-1] + rhs_j.shape[-1]],
                          dtype=jnp.result_type(lhs_indices, rhs_indices))
  out_indices = out_indices.at[:, :, :lhs_j.shape[-1]].set(lhs_j[:, None])
  out_indices = out_indices.at[:, :, lhs_j.shape[-1]:].set(rhs_j[None, :])
  out_indices = out_indices.reshape(len(out_data), out_indices.shape[-1])
  # Note: we do not eliminate zeros here, because it can cause issues with autodiff.
  # See https://github.com/jax-ml/jax/issues/10163.
  return _bcoo_sum_duplicates(out_data, out_indices, spinfo=SparseInfo(shape=out_shape), nse=out_nse)

