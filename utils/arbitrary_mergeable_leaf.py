
def arbitrary_mergeable_leaf(min_num_dims, args, kwargs):
  for a in jax.tree_util.tree_leaves(args):
    if ndim_at_least(a, min_num_dims):
      return a
  for k in jax.tree_util.tree_leaves(kwargs):
    if ndim_at_least(k, min_num_dims):
      return k
  # Couldn't find a satisfactory leaf.
  return None

