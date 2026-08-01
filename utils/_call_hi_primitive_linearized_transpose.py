
def _call_hi_primitive_linearized_transpose(cts_flat, *args, _prim,
                                            residuals_tree, nz_in_flat):
  residuals_flat, accums_flat = split_list(args, [residuals_tree.num_leaves])
  residuals = tree_unflatten(residuals_tree, residuals_flat)
  accums_flat_ = iter(accums_flat)
  accums_flat = [next(accums_flat_) if nz else ad.NullAccum(aval.to_ct_aval())
                 for aval, nz in zip(_prim.in_avals_flat, nz_in_flat)]
  assert next(accums_flat_, None) is None
  accums = tree_unflatten(_prim.in_tree, accums_flat)
  cts = tree_unflatten(_prim.out_tree, cts_flat)
  none = _prim.vjp_bwd(residuals, cts, *accums)
  assert none is None

