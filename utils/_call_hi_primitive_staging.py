
def _call_hi_primitive_staging(trace, source_info, *args_flat, _prim):
  trace.frame.is_high = True
  args = tree_unflatten(_prim.in_tree, args_flat)
  ans = _prim.staging(trace, source_info, *args)
  return tree_leaves_checked(_prim.out_tree, ans)

