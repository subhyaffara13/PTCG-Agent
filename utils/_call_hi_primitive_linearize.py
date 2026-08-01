
def _call_hi_primitive_linearize(is_vjp, nz_in_flat, *args_flat, _prim):
  args = tree_unflatten(_prim.in_tree, args_flat)
  nzs_in = tree_unflatten(_prim.in_tree, nz_in_flat)
  if is_vjp:
    ans, residuals, *maybe_nzs_out = _prim.vjp_fwd(nzs_in, *args)
    linearized = partial(fake_linear_op, _prim, nz_in_flat)
  else:
    ans, residuals, *maybe_nzs_out = _prim.lin(nzs_in, *args)
    linearized = partial(flatten_user_linearized, _prim)
  ans_flat = tree_leaves_checked(_prim.out_tree, ans)
  nzs_out = maybe_nzs_out[0] if maybe_nzs_out else True
  nzs_out_flat = broadcast_prefix(nzs_out, ans)
  return ans_flat, nzs_out_flat, residuals, linearized

