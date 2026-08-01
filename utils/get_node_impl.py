
def get_node_impl(x: Node) -> NodeImpl[Node, tp.Any, tp.Any] | None:
  if isinstance(x, Variable):
    return None

  node_type = type(x)

  if node_type in GRAPH_REGISTRY:
    return GRAPH_REGISTRY[node_type]
  elif node_type in PYTREE_REGISTRY:
    return PYTREE_REGISTRY[node_type]
  elif node_type in JAX_PYTREE_REGISTRY or issubclass(node_type, tuple):
    return PYTREE_NODE_IMPL  # type: ignore
  else:
    return None

