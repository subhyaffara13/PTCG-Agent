
def is_node_type(x: type[tp.Any]) -> bool:
  return x in GRAPH_REGISTRY or x in PYTREE_REGISTRY or x is GenericPytree

