
def fake_linear_op(prim, nz_in_flat, rs, *tangents):
  residuals_flat, residuals_tree = tree_flatten(rs)
  assert nz_in_flat == [not isinstance(t, ad_util.Zero) for t in tangents]
  nz_tangents = tree_leaves(tangents)
  return call_hi_primitive_linearized_p.bind(
      *residuals_flat, *nz_tangents, residuals_tree=residuals_tree, _prim=prim,
      nz_in_flat=tuple(nz_in_flat))

