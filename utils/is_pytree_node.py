
def is_pytree_node(
  x: tp.Any, *, check_graph_registry: bool = True,
) -> bool:
  if check_graph_registry and type(x) in GRAPH_REGISTRY:
    return False
  elif isinstance(x, Variable):
    return False
  elif type(x) in JAX_PYTREE_REGISTRY:
    return True
  elif isinstance(x, tuple):
    return True
  else:
    return False

