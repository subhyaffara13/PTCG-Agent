
def broadcast_prefix_map(
  f: tp.Callable[..., tp.Any],
  prefix_tree: tp.Any,
  full_tree: tp.Any,
  *rest: tp.Any,
  is_leaf: tp.Callable[[tp.Any], bool] | None = None,
  prefix_leaf: tp.Callable[[tp.Any], bool] | None = None,
) -> tp.Any:
  _, prefix_leaves = broadcast_prefix2(prefix_tree, full_tree, is_leaf=is_leaf, prefix_leaf=prefix_leaf)
  full_leaves_with_path, treedef = jax.tree.flatten_with_path(full_tree, is_leaf=is_leaf)
  rest_flat = [treedef.flatten_up_to(r) for r in rest]
  out_leaves = []
  for (path, full_leaf), p_leaf, *r_leaves in zip(full_leaves_with_path, prefix_leaves, *rest_flat):
    out_leaf = f(path, p_leaf, full_leaf, *r_leaves)
    out_leaves.append(out_leaf)
  return jax.tree.unflatten(treedef, out_leaves)

