
def leaf_is_placeholder(leaf: Any) -> bool:
  """Determines if `leaf` represents a placeholder for a non-aggregated value."""
  return isinstance(leaf, str) and (
      leaf.startswith(_PLACEHOLDER_PREFIX)
      or leaf.startswith(_AGGREGATED_PREFIX)
  )

