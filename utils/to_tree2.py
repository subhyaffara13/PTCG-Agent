
def to_tree2(
    tree,
    /,
    *,
    prefix: tp.Any = Missing,
    check_aliasing: bool = True,
    prefix_fn: tp.Callable[[PathParts, tp.Any], tp.Any] | None = None,
) -> tp.Any:
  """to_tree2 has two main tasks:

  1. Convert all graph nodes to TreeState (a tree representation).
  2. Check all Variables are aliased consistently given the prefix tree,
    e.g. vmap's in/out_axes arguments.

  Each NodeState contains the `GraphDef` and State for each object, these
  are generated using `graphlib.flatten`. `extract.broadcast_prefix` is used
  to calculate the prefix for each node, `check_consistent_aliasing2` traverses
  the nodes subgraph and checks for Variable aliasing.
  """
  ref_index: graphlib.RefMap = graphlib.RefMap()

  def _to_node_states(leaf):
    if not (graphlib.is_graph_node(leaf) or isinstance(leaf, variablelib.Variable)):
      return leaf
    graphdef, flat_state = graphlib.flatten(
      leaf, ref_index=ref_index, graph=True
    )
    (state,) = graphlib._to_nested_state(graphdef, (flat_state,))
    return TreeState(graphdef, state, prefix_fn=Opaque(prefix_fn))

  is_leaf = lambda x: (
    isinstance(x, variablelib.Variable) or graphlib.is_graph_node(x)
  )

  if prefix is Missing or prefix is None:
    return jax.tree.map(_to_node_states, tree, is_leaf=is_leaf)

  leaf_prefixes = broadcast_prefix(
      prefix,
      tree,
      prefix_is_leaf=lambda x: x is None
      or isinstance(x, TreeState)
      or is_leaf(x),
      tree_is_leaf=is_leaf,
  )
  leaf_paths, treedef = jax.tree_util.tree_flatten_with_path(tree, is_leaf=is_leaf)

  assert len(leaf_paths) == len(leaf_prefixes)
  leaves_out = []
  node_prefixes: dict[int, list[tuple[PathParts, tp.Any]]] = {}

  for (keypath, leaf), leaf_prefix in zip(leaf_paths, leaf_prefixes):
    if is_leaf(leaf):
      if check_aliasing:
        base_path = graphlib.jax_to_nnx_path(keypath)
        check_consistent_aliasing2(
          leaf, leaf_prefix, base_path=base_path, node_prefixes=node_prefixes
        )
      leaves_out.append(_to_node_states(leaf))
    else:
      leaves_out.append(leaf)

  return jax.tree.unflatten(treedef, leaves_out)

