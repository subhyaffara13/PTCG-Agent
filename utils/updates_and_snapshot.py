
def updates_and_snapshot(args: A) -> tuple[A, A]:
  is_leaf = lambda x: isinstance(x, variablelib.Variable)
  leaves, treedef = jax.tree.flatten(args, is_leaf=is_leaf)
  updates_leaves: list[variablelib.Variable | Mask] = []
  snapshot_leaves: list[variablelib.Variable | Mask] = []
  for leaf in leaves:
    if isinstance(leaf, variablelib.Variable):
      updates_leaves.append(leaf)
      # don't snapshot hijax or ref Variables as their updates are automatically
      # masked out in mask_variable_updates. However, the leaf is kept in the
      # updates to check for aliasing. This avoids a copy operation which has
      # significance for ref Variables.
      if leaf.hijax or leaf.ref:
        snapshot_leaves.append(Mask())
      else:
        snapshot_leaves.append(leaf.copy())
    else:
      updates_leaves.append(Mask())
      snapshot_leaves.append(Mask())
  updates = jax.tree.unflatten(treedef, updates_leaves)
  snapshot = jax.tree.unflatten(treedef, snapshot_leaves)
  return updates, snapshot

