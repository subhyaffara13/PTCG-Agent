
def is_graph_node(x: tp.Any) -> bool:
  return (
    type(x) in GRAPH_REGISTRY
    or variablelib.is_array_ref(x)
    or isinstance(x, Variable)
  )

