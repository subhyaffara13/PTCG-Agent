
def is_node(x: tp.Any) -> bool:
  if isinstance(x, Variable):
    return False
  if type(x) in GRAPH_REGISTRY:
    return True
  return is_pytree_node(x)

