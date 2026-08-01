
def _call_hi_primitive_batcher(axis_data, args_flat, dims_flat, _prim):
  args = tree_unflatten(_prim.in_tree, args_flat)
  dims = tree_unflatten(_prim.in_tree, dims_flat)
  ans, dims = _prim.batch(axis_data, args, dims)
  ans_flat = tree_leaves_checked(_prim.out_tree, ans)
  dims_flat = _prim.out_tree.flatten_up_to(dims)
  return ans_flat, dims_flat

