
def clear_non_graph_nodes(tree):
  return jax.tree.map(
    lambda x: x
    if graphlib.is_graph_node(x) or isinstance(x, variablelib.Variable)
    else None,
    tree,
    is_leaf=lambda x: isinstance(x, variablelib.Variable)
    or graphlib.is_graph_node(x),
  )

