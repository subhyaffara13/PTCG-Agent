
def _call_hi_primitive_jvp(primals, tangents, *, _prim):
  primals = tree_unflatten(_prim.in_tree, primals)
  tangents = tree_unflatten(_prim.in_tree, tangents)
  out_primals, out_tangents = _prim.jvp(primals, tangents)
  out_primals_flat = tree_leaves_checked(_prim.out_tree, out_primals)
  out_tangents_flat = _prim.out_tree.flatten_up_to(out_tangents)
  return out_primals_flat, out_tangents_flat

