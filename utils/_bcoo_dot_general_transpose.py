
def _bcoo_dot_general_transpose(ct, lhs_data, lhs_indices, rhs, *, dimension_numbers,
                                preferred_element_type, lhs_spinfo: SparseInfo):
  assert not ad.is_undefined_primal(lhs_indices)
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_ndim = len(lhs_spinfo.shape)
  rhs_ndim = rhs.aval.ndim if ad.is_undefined_primal(rhs) else rhs.ndim
  lhs_kept = remaining(range(lhs_ndim), lhs_contract, lhs_batch)
  rhs_kept = remaining(range(rhs_ndim), rhs_contract, rhs_batch)
  ans_batch, ans_lhs, ans_rhs = map(list, ranges_like(lhs_batch, lhs_kept, rhs_kept))
  if ad.is_undefined_primal(lhs_data):
    dims: DotDimensionNumbers = ((ans_rhs, rhs_kept), (ans_batch, rhs_batch))
    lhs_contract_sorted_by_rhs = list(np.take(lhs_contract, np.argsort(rhs_contract)))
    permutation = list(lhs_batch) + lhs_kept + lhs_contract_sorted_by_rhs
    out_axes = list(map(int, np.argsort(permutation)))

    # Determine whether efficient approach is possible:
    placeholder_data = jnp.zeros((lhs_indices.ndim - 2) * (1,) + (lhs_indices.shape[-2],))
    placeholder_shape = tuple(lhs_indices.shape[:-2]) + lhs_indices.shape[-1] * (1,)
    try:
      _validate_permutation(placeholder_data, lhs_indices, permutation, placeholder_shape)
    except NotImplementedError:
      indices_can_be_untransposed = False
    else:
      indices_can_be_untransposed = True

    # TODO(jakevdp): explore implementing the efficient approach without actually un-transposing
    # the indices. Could this be done by un-permuting ct, rhs, and dims?

    if indices_can_be_untransposed:
      # Efficient approach: (1) un-transpose indices, (2) compute SDDMM, (3) re-transpose result.
      _, lhs_indices_T = _bcoo_transpose(placeholder_data, lhs_indices, permutation=permutation,
                                         spinfo=SparseInfo(placeholder_shape))
      result_T_shape = tuple(placeholder_shape[i] for i in permutation)
      result_T = bcoo_dot_general_sampled(ct, rhs, lhs_indices_T, dimension_numbers=dims)
      result, _ = _bcoo_transpose(result_T, lhs_indices_T, permutation=out_axes,
                                  spinfo=SparseInfo(result_T_shape))
    else:
      # Fallback to direct approach when above is not possible.
      out_dense_T = lax.dot_general(ct, rhs, dimension_numbers=dims)
      out_dense = lax.transpose(out_dense_T, out_axes)
      result = _bcoo_extract(lhs_indices, out_dense)
    result = _unbroadcast(lhs_data.aval, result)
    return result, lhs_indices, rhs
  else:
    dims = ((lhs_kept, ans_lhs), (lhs_batch, ans_batch))
    rhs_contract_sorted_by_lhs = list(np.take(rhs_contract, np.argsort(lhs_contract)))
    out_axes = list(np.argsort(list(rhs_batch) + rhs_contract_sorted_by_lhs + rhs_kept))
    result = _bcoo_dot_general(lhs_data, lhs_indices, ct, lhs_spinfo=lhs_spinfo,
                               preferred_element_type=preferred_element_type,
                               dimension_numbers=dims)
    return lhs_data, lhs_indices, lax.transpose(result, out_axes)

