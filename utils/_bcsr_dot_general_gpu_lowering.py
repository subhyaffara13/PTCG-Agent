
def _bcsr_dot_general_gpu_lowering(
    # csr_matvec_lowering, csr_matmat_lowering,
    ctx, lhs_data, lhs_indices, lhs_indptr, rhs, *, dimension_numbers,
    preferred_element_type, lhs_spinfo: SparseInfo, target_name_prefix):

  if not config.bcoo_cusparse_lowering.value:
    return _bcsr_dot_general_default_lowering(
      ctx, lhs_data, lhs_indices, lhs_indptr, rhs,
      dimension_numbers=dimension_numbers,
      preferred_element_type=preferred_element_type,
      lhs_spinfo=lhs_spinfo)

  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_data_aval, lhs_indices_aval, lhs_indptr_aval, rhs_aval = ctx.avals_in
  props = _validate_bcsr(
      lhs_data_aval, lhs_indices_aval, lhs_indptr_aval, lhs_spinfo.shape)

  use_default_lowering = False
  dtype = lhs_data_aval.dtype
  # TODO(vanderplas, tianjianlu): lower batched matmuls to GPU
  if lhs_batch or rhs_batch:
    # batch dimensions in dot_general are not supported
    use_default_lowering = True
  elif (lhs_data_aval.dtype != rhs_aval.dtype):
    use_default_lowering = True
  elif preferred_element_type is not None and preferred_element_type != lhs_data_aval.dtype:
    use_default_lowering = True
  elif len(lhs_spinfo.shape) != 2 or rhs_aval.ndim not in [1, 2]:
    # only matmat / matvec supported
    use_default_lowering = True
  elif props.n_batch or props.n_dense:
    # batch and dense dimensions in BCSR not supported
    use_default_lowering = True
  elif list(lhs_contract) != [1]:
    # cusparse cannot contract over more than one dimension
    use_default_lowering = True
  elif dtype not in [np.float32, np.float64, np.complex64, np.complex128]:
    # This would be supported if not for the dtype.
    warnings.warn(f'bcsr_dot_general cusparse/hipsparse lowering not available '
                  f'for {dtype=}. Falling back to default implementation.',
                  CuSparseEfficiencyWarning)
    use_default_lowering = True

  if use_default_lowering:
    return _bcsr_dot_general_default_lowering(
      ctx, lhs_data, lhs_indices, lhs_indptr, rhs,
      dimension_numbers=dimension_numbers,
      preferred_element_type=preferred_element_type,
      lhs_spinfo=lhs_spinfo)

  # Account for a bug in cusparse: it references indices and data beyond
  # the extent of indptr.
  lhs_data, lhs_indices = _bcsr_correct_out_of_bound_indices_lowered(
    ctx, lhs_data, lhs_indices, lhs_indptr, rhs, shape=lhs_spinfo.shape)

  sub_ctx = ctx
  if rhs_aval.ndim == 1:
    dot_general_fn = _lowerings._csr_spmv_gpu_lowering
  elif rhs_aval.ndim == 2:
    dot_general_fn = _lowerings._csr_spmm_gpu_lowering
    if rhs_contract[0] == 1:
      rhs = hlo.transpose(rhs, permutation=mlir.dense_int_array([1, 0]))
      *avals_in, rhs_aval = sub_ctx.avals_in
      rhs_aval = core.ShapedArray(
          shape=(rhs_aval.shape[1], rhs_aval.shape[0]), dtype=rhs_aval.dtype)
      sub_ctx = sub_ctx.replace(avals_in=[*avals_in, rhs_aval])
  else:
    raise ValueError(f"rhs has to be 1d or 2d; get {rhs_aval.ndim}d.")

  return dot_general_fn(sub_ctx, lhs_data, lhs_indices, lhs_indptr, rhs,
                        shape=lhs_spinfo.shape, transpose=False,
                        target_name_prefix=target_name_prefix)

