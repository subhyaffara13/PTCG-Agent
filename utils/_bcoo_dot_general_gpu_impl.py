
def _bcoo_dot_general_gpu_impl(lhs_data, lhs_indices, rhs, *,
                               dimension_numbers, preferred_element_type,
                               lhs_spinfo):
  if not config.bcoo_cusparse_lowering.value:
    return _bcoo_dot_general_impl(lhs_data, lhs_indices, rhs,
        dimension_numbers=dimension_numbers,
        preferred_element_type=preferred_element_type,
        lhs_spinfo=lhs_spinfo)

  (lhs_contract, rhs_contract), (lhs_batch, _) = dimension_numbers
  n_batch, n_sparse, n_dense, _ = _validate_bcoo(
      lhs_data, lhs_indices, lhs_spinfo.shape)
  coo_matmul_p = coo_spmv_p if rhs.ndim == 1 else coo_spmm_p

  out_aval = _bcoo_dot_general_abstract_eval(
    lhs_data, lhs_indices, rhs,
    dimension_numbers=dimension_numbers,
    preferred_element_type=preferred_element_type,
    lhs_spinfo=lhs_spinfo)

  if out_aval.dtype not in CUSPARSE_DATA_DTYPES:
    return _bcoo_dot_general_impl(lhs_data, lhs_indices, rhs,
        dimension_numbers=dimension_numbers,
        preferred_element_type=preferred_element_type,
        lhs_spinfo=lhs_spinfo)

  lhs_data = lhs_data.astype(out_aval.dtype)
  rhs = rhs.astype(out_aval.dtype)

  # TODO(jakevdp, tianjianlu): add support for batched lowerings
  if (len(lhs_contract) == 1 and len(lhs_batch) == 0 and rhs.ndim in (1, 2)
      and (n_batch, n_sparse, n_dense) == (0, 1, 0)
      and not _bcoo_dot_general_fallback(lhs_data, lhs_indices, lhs_spinfo)):
    row, col = jnp.zeros(lhs_indices.shape[0], lhs_indices.dtype), lhs_indices.ravel()
    transpose = False
    shape = (1, *lhs_spinfo.shape)
    row, col, shape = _coo_correct_out_of_bound_indices(row, col, shape, transpose)
    out = coo_matmul_p.bind(lhs_data, row, col,
                            rhs.T if rhs_contract[0] == 1 else rhs,
                            transpose=transpose, shape=shape)
    return out[0]
  elif (len(lhs_contract) == 1 and len(lhs_batch) == 0 and rhs.ndim in (1, 2)
        and (n_batch, n_sparse, n_dense) == (0, 2, 0)
        and not _bcoo_dot_general_fallback(lhs_data, lhs_indices, lhs_spinfo)):
    row, col = lhs_indices[:, 0], lhs_indices[:, 1]
    transpose = (lhs_contract[0] == 0)
    shape = lhs_spinfo.shape
    row, col, shape = _coo_correct_out_of_bound_indices(row, col, shape, transpose)
    out = coo_matmul_p.bind(lhs_data, row, col,
                            rhs.T if rhs_contract[0] == 1 else rhs,
                            transpose=transpose, shape=shape)
    return out[:-1]
  else:
    return _bcoo_dot_general_impl(lhs_data, lhs_indices, rhs,
        dimension_numbers=dimension_numbers, lhs_spinfo=lhs_spinfo,
        preferred_element_type=preferred_element_type)

