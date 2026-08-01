
def get_node_impl_for_type(
  x: type[Node],
) -> NodeImpl[Node, tp.Any, tp.Any] | None:
  if x is GenericPytree:
    return PYTREE_NODE_IMPL  # type: ignore
  elif x in PYTREE_REGISTRY:
    return PYTREE_REGISTRY[x]
  elif x in GRAPH_REGISTRY:
    return GRAPH_REGISTRY[x]
  else:
    return None

