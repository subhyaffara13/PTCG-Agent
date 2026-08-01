
def _dma_flatten(*args):
  flat_tree = tree_util.FlatTree.flatten(args)
  return flat_tree.vals, flat_tree.tree

