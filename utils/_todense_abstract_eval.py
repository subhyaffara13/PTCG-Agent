
def _todense_abstract_eval(*bufs, tree):
  arr = tree_util.tree_unflatten(tree, bufs)
  if isinstance(arr, core.ShapedArray):
    return arr
  return core.ShapedArray(arr.shape, arr.dtype, weak_type=dtypes.is_weakly_typed(arr.data))

