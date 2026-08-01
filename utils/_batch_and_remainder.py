
def _batch_and_remainder(x, batch_size: int):
  leaves, treedef = tree_flatten(x)
  if not leaves:
    return x, None
  if batch_size == 0:
    num_batches, remainder = 0, leaves[0].shape[0]
  else:
    num_batches, remainder = divmod(leaves[0].shape[0], batch_size)
  batch_elems = num_batches * batch_size
  if num_batches == 0:
    remainder_leaves = [_remainder_leaf(leaf, batch_elems) for leaf in leaves]
    return None, treedef.unflatten(remainder_leaves)
  elif remainder:
    scan_leaves, remainder_leaves = unzip2(
        [(_scan_leaf(leaf, batch_elems, num_batches, batch_size),
          _remainder_leaf(leaf, batch_elems)) for leaf in leaves])
    return treedef.unflatten(scan_leaves), treedef.unflatten(remainder_leaves)
  else:
    scan_leaves = tuple(_scan_leaf(leaf, batch_elems, num_batches, batch_size)
                        for leaf in leaves)
    return treedef.unflatten(scan_leaves), None

