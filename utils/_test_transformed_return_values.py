
def _test_transformed_return_values(tree, method_name):
  """Tests whether the return value contains any Modules or Variables."""
  impure = any(
    map(
      lambda x: isinstance(x, (Module, Variable)),
      jax.tree_util.tree_leaves(tree),
    )
  )
  if impure:
    raise errors.TransformedMethodReturnValueError(method_name)

