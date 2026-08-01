
def tree_split(mask, tree):
  lhs = tree_map(lambda l, x: x if l else None, mask, tree)
  rhs = tree_map(lambda l, x: None if l else x, mask, tree)
  return lhs, rhs

