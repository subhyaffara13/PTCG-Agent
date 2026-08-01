
def _jacfwd_unravel(input_pytree, output_pytree_leaf, arr):
  axis = -1 % arr.ndim
  arr_s = core.typeof(arr).sharding.spec
  specs = tree_map(
      lambda l: P(*arr_s[:axis], *[None] * len(np.shape(l)), *arr_s[axis+1:]),
      input_pytree)
  return _unravel_array_into_pytree(
    input_pytree, axis, output_pytree_leaf, arr, specs)

