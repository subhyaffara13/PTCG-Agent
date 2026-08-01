
def _call_hi_primitive_to_lojax(*args_flat, _prim):
  args = tree_unflatten(_prim.in_tree, args_flat)
  ans = _prim.expand(*args)
  return tree_leaves_checked(_prim.out_tree, ans)

