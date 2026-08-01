
def _flatten_to_partial_state(
    arg: tp.Any,
    ref_index: graphlib.RefMap | None,
) -> PartialState:
  if ref_index is not None:
    graphdef, flat_state = graphlib.flatten(arg, ref_index=ref_index, graph=True)
    return PartialState(treedef=graphdef, leaves=flat_state.leaves)
  is_leaf = lambda x: isinstance(x, variablelib.Variable)
  leaves, treedef = jax.tree.flatten(arg, is_leaf=is_leaf)
  return PartialState(treedef=treedef, leaves=leaves)

