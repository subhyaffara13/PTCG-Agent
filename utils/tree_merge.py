
def tree_merge(mask, lhs_tree, rhs_tree):
  return tree_map(lambda l, x_l, x_r: x_l if l else x_r,
                  mask, lhs_tree, rhs_tree)

