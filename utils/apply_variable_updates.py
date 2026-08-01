
def apply_variable_updates(args_tree: A, updates_tree: A):
  is_leaf = lambda x: isinstance(x, variablelib.Variable) or isinstance(x, Mask)
  args_leaves = jax.tree.leaves(args_tree, is_leaf=is_leaf)
  _, treedef = jax.tree.flatten(args_tree, is_leaf=is_leaf)
  updates_leaves = treedef.flatten_up_to(updates_tree)
  for variable, update in zip(args_leaves, updates_leaves, strict=True):
    if isinstance(update, variablelib.Variable):
      assert isinstance(variable, variablelib.Variable)
      variable.update_from_state(update)

