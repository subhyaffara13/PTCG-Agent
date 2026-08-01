
def _reconsile_index_mapping(tree_to_fix, example_tree):
  def f(a, b):
    if not isinstance(a, extract.NodeStates) or not isinstance(
      a._graphdef, graphlib.GraphDef
    ):
      return a
    return dataclasses.replace(
      a, _graphdef=a._graphdef.with_matching_outer_index(b._graphdef)
    )

  return jax.tree.map(f, tree_to_fix, example_tree,
                      is_leaf=lambda x: isinstance(x, extract.NodeStates))

