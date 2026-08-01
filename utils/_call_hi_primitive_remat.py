
def _call_hi_primitive_remat(policy, *args_flat, _prim):
  args = tree_unflatten(_prim.in_tree, args_flat)
  out, rem_ = _prim.remat(policy, *args)
  def rem(*args_flat):
    args = tree_unflatten(_prim.in_tree, args_flat)
    out = rem_(*args)
    return tree_leaves_checked(_prim.out_tree, out)
  return tree_leaves_checked(_prim.out_tree, out), rem

