
def ltg_abstract_eval(arr, *, global_mesh, pspec):
  return _local_to_global_aval(
      core.ShapedArray(arr.shape, arr.dtype), global_mesh, pspec)

