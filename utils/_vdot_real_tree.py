
def _vdot_real_tree(x, y):
  return sum(tree_leaves(tree_map(_vdot_real_part, x, y)))

