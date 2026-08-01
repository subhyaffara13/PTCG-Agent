
def apply_function(tree, function):
  """Applies the given function to every leaf in tree.

  Args:
    tree: a nested dict where every leaf is a sharded jax.Array.
    function: a function accepting an array and returning jax.Array.

  Returns:
    a transformed sharded array tree.
  """

  def f(arr):
    return pjit.pjit(function)(arr)

  return jax.tree.map(f, tree)

