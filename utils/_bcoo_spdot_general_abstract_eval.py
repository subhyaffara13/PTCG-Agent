
def _bcoo_spdot_general_abstract_eval(lhs_data, lhs_indices, rhs_data, rhs_indices, *, lhs_spinfo: SparseInfo, rhs_spinfo: SparseInfo,
                                      dimension_numbers, preferred_element_type):
  lhs_shape = lhs_spinfo.shape
  rhs_shape = rhs_spinfo.shape
  out_aval = jax.jit(lax.dot_general, static_argnames=("dimension_numbers", "preferred_element_type")).eval_shape(
      jax.ShapeDtypeStruct(lhs_shape, lhs_data.dtype),
      jax.ShapeDtypeStruct(rhs_shape, rhs_data.dtype),
      dimension_numbers=dimension_numbers,
      preferred_element_type=preferred_element_type)

  lhs = _validate_bcoo(lhs_data, lhs_indices, lhs_shape)
  rhs = _validate_bcoo(rhs_data, rhs_indices, rhs_shape)
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers

  if lhs.n_dense or rhs.n_dense:
    # TODO(jakevdp): handle dense dimensions
    raise NotImplementedError("bcoo_spdot_general with dense dimensions.")

  if (lhs_batch and max(lhs_batch) >= lhs.n_batch) or (rhs_batch and max(rhs_batch) >= rhs.n_batch):
    raise NotImplementedError("bcoo_spdot_general: batch_dims must correspond to batch dimensions of the sparse representation.")

  if lhs_contracting and (min(lhs_contracting) < lhs.n_batch or max(lhs_contracting) >= lhs.n_batch + lhs.n_sparse):
    raise NotImplementedError("bcoo_spdot_general only supports contraction of sparse indices.")

  if rhs_contracting and (min(rhs_contracting) < rhs.n_batch or max(rhs_contracting) >= rhs.n_batch + rhs.n_sparse):
    raise NotImplementedError("bcoo_spdot_general only supports contraction of sparse indices.")

  if rhs.n_batch > len(rhs_batch) and lhs.n_sparse > len(lhs_contracting):
    raise ValueError("bcoo_spdot_general: cannot have unused batch dims on rhs with unused sparse dims on lhs.")

  out_nse = (
    (lhs.nse if lhs.n_sparse > len(lhs_contracting) else 1) *
    (rhs.nse if rhs.n_sparse > len(rhs_contracting) else 1)
  )

  # Ensure we're not storing more output elements than necessary.
  # TODO(jakevdp): should we warn here if output is effectively dense?
  out_n_batch = lhs.n_batch + rhs.n_batch - len(lhs_batch)
  out_nse = min(out_nse, math.prod(out_aval.shape[out_n_batch:]))

  lhs_batch_shape = np.broadcast_shapes(
    tuple(lhs_data.shape[dim] for dim in range(lhs.n_batch) if dim not in lhs_batch),
    tuple(lhs_indices.shape[dim] for dim in range(lhs.n_batch) if dim not in lhs_batch),
  )
  rhs_batch_shape = np.broadcast_shapes(
    tuple(rhs_data.shape[dim] for dim in range(rhs.n_batch) if dim not in rhs_batch),
    tuple(rhs_indices.shape[dim] for dim in range(rhs.n_batch) if dim not in rhs_batch),
  )

  data_shape = (
    *(lhs_shape[dim] for dim in lhs_batch),
    *lhs_batch_shape,
    *rhs_batch_shape,
    out_nse)
  indices_shape = (
    *(lhs_shape[dim] for dim in lhs_batch),
    *lhs_batch_shape,
    *rhs_batch_shape,
    out_nse, lhs.n_sparse + rhs.n_sparse - 2 * len(lhs_contracting))

  data_aval = core.ShapedArray(data_shape, out_aval.dtype)
  indices_aval = core.ShapedArray(indices_shape, lhs_indices.dtype)
  _validate_bcoo(data_aval, indices_aval, out_aval.shape)  # always-use-return-annotations

  return data_aval, indices_aval

