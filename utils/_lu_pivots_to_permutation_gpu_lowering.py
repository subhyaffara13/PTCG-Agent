
def _lu_pivots_to_permutation_gpu_lowering(ctx, pivots, *,
                                           permutation_size,
                                           target_name_prefix):
  del permutation_size  # unused
  rule = _linalg_ffi_lowering(f"{target_name_prefix}_lu_pivots_to_permutation",
                              num_non_batch_dims=1, column_major=False)
  return rule(ctx, pivots)

