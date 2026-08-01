
def _pbroadcast_is_async(x, axis_name, source, is_async=False):
  prim = pbroadcast_start_p if is_async else pbroadcast_p
  return tree_util.tree_map(
      partial(prim.bind, axis_name=axis_name, source=source), x)

