
def _get_discharge(x, idx, tree):
  transforms = tree_util.tree_unflatten(tree, idx)
  return transform_array(x, transforms)

