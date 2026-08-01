
def from_tree2(tree: tp.Any, /) -> tp.Any:
  index_ref = graphlib.IndexMap()

  def _from_node_states(x):
    if not isinstance(x, TreeState):
      return x
    state = graphlib._merge_to_flat_state((x.state,))
    return graphlib.unflatten(
      x.graphdef, state, index_ref=index_ref,
    )

  return jax.tree.map(
      _from_node_states,
      tree,
      is_leaf=lambda x: (
          isinstance(x, TreeState)
          or graphlib.is_graph_node(x)
          or isinstance(x, variablelib.Variable)
      ),
  )

