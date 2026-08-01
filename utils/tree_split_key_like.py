
def tree_split_key_like(
    rng_key: base.PRNGKey, target_tree: base.ArrayTree
) -> base.ArrayTree:
  """Split keys to match structure of target tree.

  Args:
    rng_key: the key to split.
    target_tree: the tree whose structure to match.

  Returns:
    a tree of rng keys.
  """
  tree_def = jax.tree.structure(target_tree)
  keys = jax.random.split(rng_key, tree_def.num_leaves)
  return jax.tree.unflatten(tree_def, keys)

