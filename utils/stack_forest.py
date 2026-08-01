
def stack_forest(forest):
  """Helper function to stack the leaves of a sequence of pytrees.

  Args:
    forest: a sequence of pytrees (e.g tuple or list) of matching structure
      whose leaves are arrays with individually matching shapes.
  Returns:
    A single pytree of the same structure whose leaves are individually
      stacked arrays.
  """
  stack_args = lambda *args: jnp.stack(args)
  return jax.tree_util.tree_map(stack_args, *forest)

