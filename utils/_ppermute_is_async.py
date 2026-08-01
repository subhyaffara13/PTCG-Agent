
def _ppermute_is_async(x, axis_name, perm, is_async=False):
  if not isinstance(axis_name, (list, tuple)):
    axis_name = (axis_name,)
  def bind(leaf):
    leaf = insert_collective_pvary(axis_name, leaf)
    prim = ppermute_start_p if is_async else ppermute_p
    return prim.bind(leaf, axis_name=axis_name, perm=tuple(map(tuple, perm)))
  return tree_util.tree_map(bind, x)

