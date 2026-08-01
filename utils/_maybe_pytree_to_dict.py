
def _maybe_pytree_to_dict(pytree: tp.Any):
  path_leaves = jax.tree_util.tree_flatten_with_path(pytree)[0]
  path_leaves = [
    (tuple(map(graphlib._key_path_to_key, path)), value)
    for path, value in path_leaves
  ]
  if len(path_leaves) < 1:
    return pytree
  elif len(path_leaves) == 1 and path_leaves[0][0] == ():
    return pytree
  else:
    return _unflatten_to_simple_structure(path_leaves, original=pytree)

