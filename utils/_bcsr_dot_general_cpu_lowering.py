
def _bcsr_dot_general_cpu_lowering(
    # csr_matvec_lowering, csr_matmat_lowering,
    ctx,
    lhs_data,
    lhs_indices,
    lhs_indptr,
    rhs,
    *,
    dimension_numbers,
    preferred_element_type,
    lhs_spinfo: SparseInfo,
):

  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_data_aval, lhs_indices_aval, lhs_indptr_aval, rhs_aval = ctx.avals_in
  props = _validate_bcsr(
      lhs_data_aval, lhs_indices_aval, lhs_indptr_aval, lhs_spinfo.shape
  )

  use_default_lowering = False
  dtype = lhs_data_aval.dtype
  if lhs_batch or rhs_batch:
    # TODO(willfroom): Add support for batched matrices.
    use_default_lowering = True
  elif lhs_data_aval.dtype != rhs_aval.dtype:
    use_default_lowering = True
  elif (
      preferred_element_type is not None
      and preferred_element_type != lhs_data_aval.dtype
  ):
    use_default_lowering = True
  elif len(lhs_spinfo.shape) != 2 or rhs_aval.ndim not in [1, 2]:
    # only matmat / matvec supported
    use_default_lowering = True
  elif props.n_batch or props.n_dense:
    # batch and dense dimensions in BCSR not supported
    use_default_lowering = True
  elif list(lhs_contract) != [1] or list(rhs_contract) != [0]:
    # TODO(willfroom): Add support for non-canonical dots.
    use_default_lowering = True
  elif lhs_indices_aval.dtype != lhs_indptr_aval.dtype:
    warnings.warn(
        "bcsr_dot_general cpu lowering not available, "
        f" {lhs_indices_aval.dtype=} and {lhs_indptr_aval.dtype=} do not match."
        " Falling back to default implementation.",
        SparseEfficiencyWarning,
    )
    use_default_lowering = True
  elif lhs_indices_aval.dtype not in [np.int32, np.int64]:
    use_default_lowering = True
    warnings.warn(
        "bcsr_dot_general cpu lowering not available for"
        f" {lhs_indices_aval.dtype=}. Falling back to default implementation.",
        SparseEfficiencyWarning,
    )
  elif dtype not in [
      np.int32,
      np.int64,
      np.float32,
      np.float64,
      np.complex64,
      np.complex128,
  ]:
    # This would be supported if not for the dtype.
    warnings.warn(
        "bcsr_dot_general cpu lowering not available "
        f"for {dtype=}. Falling back to default implementation.",
        SparseEfficiencyWarning,
    )
    use_default_lowering = True

  if use_default_lowering:
    return _bcsr_dot_general_default_lowering(
        ctx,
        lhs_data,
        lhs_indices,
        lhs_indptr,
        rhs,
        dimension_numbers=dimension_numbers,
        preferred_element_type=preferred_element_type,
        lhs_spinfo=lhs_spinfo,
    )

  return _lowerings._csr_spmm_cpu_lowering(
      ctx, lhs_data, lhs_indptr, lhs_indices, rhs
  )

