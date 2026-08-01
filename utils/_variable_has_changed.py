
def _variable_has_changed(old: Variable, new: Variable) -> bool:
  old_structure = jax.tree.structure(old)
  new_structure = jax.tree.structure(new)
  if old_structure != new_structure:  # type: ignore[operator]
    return True
  old_leaves = jax.tree.leaves(old)
  new_leaves = jax.tree.leaves(new)
  return any(o is not n for o, n in zip(old_leaves, new_leaves))

