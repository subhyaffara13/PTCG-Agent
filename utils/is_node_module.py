
def is_node_module(x: tp.Any) -> bool:
  return type(x) in GRAPH_REGISTRY

