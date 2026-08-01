
def validate_abstract_state(
    abstract_state: tree_types.PyTreeOf[tree_types.AbstractLeaf] | None,
) -> None:
  """Validates an abstract PyTree state before loading."""
  if abstract_state is None:
    return
  leaves = jax.tree.leaves(abstract_state)
  for leaf in leaves:
    if not tree_types_validation.is_supported_abstract_leaf(leaf):
      raise TypeError(
          f'Unsupported abstract leaf type for loading: `{type(leaf)}`.'
          f' Supported abstract leaf types are: {tree_types.AbstractLeaf} (or'
          f' concrete values of {tree_types.Leaf}).'
      )

