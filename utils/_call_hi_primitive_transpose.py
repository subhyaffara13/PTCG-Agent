
def _call_hi_primitive_transpose(cts_flat, *primals_flat, _prim):
  cts = tree_unflatten(_prim.out_tree, cts_flat)
  primals = tree_unflatten(_prim.in_tree, primals_flat)
  none = _prim.transpose(cts, *primals)
  assert none is None

