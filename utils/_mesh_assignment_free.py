
def _mesh_assignment_free(new_assignment, existing_assignments):
  """Determines if a given mesh axis has already been assigned."""
  new = set(jax.tree_util.tree_leaves(new_assignment))
  existing = set(jax.tree_util.tree_leaves(existing_assignments))
  new.discard(jax.sharding.PartitionSpec.UNCONSTRAINED)
  new.discard(None)
  if existing.intersection(new):
    return False
  return True

