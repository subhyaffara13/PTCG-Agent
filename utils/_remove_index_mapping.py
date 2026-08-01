
def _remove_index_mapping(tree: tp.Any):
  """Remove a fake outer_index for the input to match that of the output."""

  def per_node_state(node_state: extract.NodeStates | tp.Any):
    if not isinstance(node_state, extract.NodeStates) or not isinstance(
      node_state._graphdef, graphlib.GraphDef
    ):
      return node_state
    assert isinstance(node_state._graphdef, graphlib.GraphDef)
    node_state = dataclasses.replace(
      node_state, _graphdef=node_state._graphdef.with_no_outer_index()
    )
    return node_state

  return jax.tree.map(per_node_state, tree,
                      is_leaf=lambda x: isinstance(x, extract.NodeStates))

