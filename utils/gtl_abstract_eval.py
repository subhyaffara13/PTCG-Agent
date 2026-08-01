
def gtl_abstract_eval(arr, *, global_mesh, pspec):
  return _global_to_local_aval(
      core.ShapedArray(arr.shape, arr.dtype), global_mesh, pspec)

