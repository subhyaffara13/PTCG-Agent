
def _jacrev_unravel(output_pytree, input_pytree_leaf, arr):
  specs = tree_map(
      lambda l: P(*[None] * len(np.shape(l)), *core.typeof(arr).sharding.spec[1:]),
      output_pytree)
  return _unravel_array_into_pytree(
    output_pytree, 0, input_pytree_leaf, arr, specs)

