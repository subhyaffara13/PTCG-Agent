
def _summary_tree_map(f, tree, *rest):
  return jax.tree_util.tree_map(f, tree, *rest, is_leaf=lambda x: x is None)

