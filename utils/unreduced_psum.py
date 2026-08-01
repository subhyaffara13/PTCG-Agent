
def unreduced_psum(x, axis_name, is_async=False):
  if not isinstance(axis_name, (tuple, list)):
    axis_name = (axis_name,)
  if not axis_name:
    return x
  prim = unreduced_psum_start_p if is_async else unreduced_psum_p
  return tree_util.tree_map(
      lambda leaf: prim.bind(leaf, axes=tuple(axis_name)), x)

