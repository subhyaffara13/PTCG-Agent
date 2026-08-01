
def _bcoo_multiply_sparse(lhs_data: Array, lhs_indices: Array, rhs_data: Array, rhs_indices: Array, *,
                          lhs_spinfo: SparseInfo, rhs_spinfo: SparseInfo) -> tuple[Array, Array, Shape]:
  lhs_shape = lhs_spinfo.shape
  rhs_shape = rhs_spinfo.shape

  lhs = _validate_bcoo(lhs_data, lhs_indices, lhs_shape)
  rhs = _validate_bcoo(rhs_data, rhs_indices, rhs_shape)
  if len(lhs_shape) != len(rhs_shape):
    # Similar requirement as lax.mul:
    raise TypeError("bcoo_multiply_sparse: arrays must have same number of dimensions, "
                    f"got {lhs_shape}, {rhs_shape}")
  if lhs.n_dense != rhs.n_dense:
    raise NotImplementedError("bcoo_multiply_sparse: arrays with differing numbers of "
                              f"dense dimensions: {lhs}, {rhs}")
  n_batch = min(lhs.n_batch, rhs.n_batch)
  _mul = functools.partial(_bcoo_multiply_sparse_unbatched,
                           lhs_shape=lhs_shape[n_batch:],
                           rhs_shape=rhs_shape[n_batch:])
  _mul = nfold_vmap(_mul, n_batch)
  data, indices = _mul(lhs_data, lhs_indices, rhs_data, rhs_indices)
  return data, indices, jnp.broadcast_shapes(lhs_shape, rhs_shape)

