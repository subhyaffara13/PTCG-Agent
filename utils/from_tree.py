
def from_tree(
  tree: tp.Any,
  /,
  *,
  prefix: tp.Any = Missing,
  merge_fn: tp.Callable[
    [graphlib.MergeContext, KeyPath, Prefix, Leaf], tp.Any
  ] = merge_tree_node,
  is_node_leaf: tp.Callable[[Leaf], bool] = is_tree_node,
  is_leaf: tp.Callable[[Leaf], bool] = is_tree_node,
  map_non_graph_nodes: bool = False,
  is_inner: bool | None = None,
  ctxtag: tp.Hashable | None = None,
) -> tp.Any:
  if prefix is Missing or prefix is None:
    # fast path, no need for prefix broadcasting or consistent aliasing checks
    with graphlib.merge_context(ctxtag, is_inner) as merge_ctx:

      def maybe_split(x):
        if (
          map_non_graph_nodes
          or is_node_leaf(x)
          or isinstance(x, variablelib.Variable)
        ):
          return merge_fn(merge_ctx, (), prefix, x)
        return x

      return jax.tree.map(maybe_split, tree, is_leaf=is_leaf)
  leaf_prefixes = broadcast_prefix(
    prefix,
    tree,
    prefix_is_leaf=lambda x: x is None or is_leaf(x),
    tree_is_leaf=is_leaf,
  )
  leaf_keys, treedef = jax.tree_util.tree_flatten_with_path(
    tree, is_leaf=is_leaf
  )
  assert len(leaf_keys) == len(leaf_prefixes)
  leaves_out = []

  with graphlib.merge_context(ctxtag, is_inner) as merge_ctx:
    for (keypath, leaf), leaf_prefix in zip(leaf_keys, leaf_prefixes):
      if (
        map_non_graph_nodes
        or is_node_leaf(leaf)
        or isinstance(leaf, variablelib.Variable)
      ):
        leaf = merge_fn(merge_ctx, keypath, leaf_prefix, leaf)
      leaves_out.append(leaf)

  pytree_out = jax.tree.unflatten(treedef, leaves_out)
  return pytree_out

