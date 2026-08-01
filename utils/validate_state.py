
def validate_state(state: tree_types.PyTreeOf[tree_types.Leaf]) -> None:
  """Validates that all leaves of the PyTree are supported leaf types."""
  leaves = jax.tree.leaves(state)
  for leaf in leaves:
    if not tree_types_validation.is_supported_leaf(leaf):
      raise ValueError(
          f'Unsupported leaf type for saving: `{type(leaf)}`. Supported leaf'
          f' types are: {tree_types.Leaf}.'
      )

