
def custom_vjp_primal_tree_values(tree):
  """Strips away perturbation information from forward rule arguments.

  This is a helper function for user with the ``symbolic_zeros`` option to
  the ``defvjp`` method of a ``custom_vjp``-decorated function.

  In ``symbolic_zeros`` mode, the custom forward rule receives arguments
  whose pytree leaves are records with a ``value`` attribute that carries
  the primal argument. This is a way to convert such argument trees back to
  their original form, replacing each such record with its carried value at
  each leaf.
  """
  def value(leaf):
    if type(leaf) is not CustomVJPPrimal:
      raise TypeError(f"unexpected leaf type {type(leaf)}")
    return leaf.value
  return tree_map(value, tree)

