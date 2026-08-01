
def _tree_broadcast(a, b, is_leaf=lambda x: x is None):
  """Broadcast the prefix tree `a` to the full tree `b`

  Uses `flatten_axes` for better error messages on mismatched arity but allowing
  for custom is_leaf in the `a` and `b` trees.
  """
  a_leaves, a_struct = jax.tree.flatten(a, is_leaf=is_leaf)
  a_idx2leaf_map = dict(enumerate(a_leaves))
  a_idx = jax.tree.unflatten(a_struct, a_idx2leaf_map.keys())
  a_idx_broadcast = flatten_axes("tree_broadcast",
                                 jax.tree.structure(b, is_leaf=is_leaf), a_idx)
  return jax.tree.map(lambda i: a_idx2leaf_map[i], a_idx_broadcast)

