
def _add_fake_index_mapping(tree: tp.Any):
  def per_node_state(node_state: extract.NodeStates | tp.Any):
    if not isinstance(node_state, extract.NodeStates) or not isinstance(
      node_state._graphdef, graphlib.GraphDef
    ):
      return node_state

    return dataclasses.replace(
      node_state, _graphdef=node_state._graphdef.with_same_outer_index()
    )

  return jax.tree.map(per_node_state, tree,
                      is_leaf=lambda x: isinstance(x, extract.NodeStates))

