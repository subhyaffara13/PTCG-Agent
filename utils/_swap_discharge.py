
def _swap_discharge(x, val, idx, tree):
  transforms = tree_util.tree_unflatten(tree, idx)
  return transform_swap_array(x, transforms, val)

