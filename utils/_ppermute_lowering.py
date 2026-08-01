
def _ppermute_lowering(ctx, x, *, axis_name, perm):
  full_perm, other_args = _pcollectives_lowering_common(
      ctx, axis_name=axis_name, perm=perm, op_name="ppermute"
  )
  return hlo.CollectivePermuteOp(
      x, mlir.dense_int_elements(full_perm), **other_args).results

